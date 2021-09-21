import asyncio
import random
from asyncio import Task
from decimal import Decimal
from itertools import chain
from logging import getLogger

from taurus.config import MixerConfig
from taurus.domain import Address, PendingDepositMix, PendingSettlementMix
from taurus.gemini_client import GeminiClient
from taurus.spreaders import Spreader

_logger = getLogger(__name__)


class Mixer:
    def __init__(
        self,
        gemini_client: GeminiClient,
        spreader: Spreader,
        house_address: Address,
        config: MixerConfig,
    ):
        self._gemini_client = gemini_client
        self._spreader = spreader
        self._house_address = house_address
        self._config = config
        self._pending_mixes: list[PendingSettlementMix] = []
        self._tasks: list[Task] = [asyncio.create_task(self._start_mixing(), name=f"mix-{house_address}")]
        _logger.info(f"Started mixing with house address {house_address}.")

    def watch(self, mix: PendingDepositMix):
        self._tasks.append(asyncio.create_task(self._watch(mix), name=f"watch-{mix.deposit_address}"))

    def stop(self):
        for task in self._tasks:
            if not task.done():
                task.cancel()
                _logger.info("Successfully cancelled task %s.", task.get_name())

    async def _watch(self, mix: PendingDepositMix):
        deposit_address = mix.deposit_address
        _logger.info(f"Now watching {deposit_address}.")

        while True:
            address_info = await self._gemini_client.address_info(deposit_address)
            balance = address_info.json()["balance"]
            if Decimal(balance) > 0:
                _logger.info(f"Found {balance} coins in {deposit_address}.")
                break

            else:
                _logger.info(f"Nothing found in {deposit_address}.")

            await asyncio.sleep(self._config.deposit_poll_interval)

        await self._gemini_client.send_jobcoins(deposit_address, self._house_address, balance)
        _logger.info(f"{balance} jobcoins were transferred to {deposit_address}. Stopped watching.")

        new_mix = PendingSettlementMix(mix.user_addresses, deposit_address, Decimal(balance))
        self._pending_mixes.append(new_mix)

    async def _start_mixing(self):
        while True:
            if len(self._pending_mixes) >= self._config.minimum_pending_settlements:
                await self._settle()

            await asyncio.sleep(self._config.house_poll_interval)

    async def _settle(self):
        transactions = chain.from_iterable(map(self._spreader, self._pending_mixes))
        coroutines = []
        for transaction in transactions:
            amount = format(transaction.amount, "f")
            coroutine = self._gemini_client.send_jobcoins(self._house_address, transaction.deposit_address, amount)
            coroutines.append(coroutine)

            # TODO: Handle failures in sending Jobcoins.

        random.shuffle(coroutines)
        await asyncio.gather(*coroutines)
        _logger.info(f"Done settling {len(self._pending_mixes)} pending mixes.")
        self._pending_mixes = []

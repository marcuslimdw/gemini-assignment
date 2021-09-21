import asyncio
import logging
from decimal import getcontext
from logging import INFO

from aioconsole import aprint

from taurus.config import MixerConfig
from taurus.domain import PendingDepositMix
from taurus.gemini_client import GeminiClient
from taurus.mixer import Mixer
from taurus.spreaders import spread_evenly
from taurus.user_io import get_user_addresses
from taurus.util import create_address

log_file = "taurus.log"
log_format = "%(asctime)s %(levelname)-8s: %(message)s"
date_format = "%m/%d/%Y %H:%M:%S"
logging.basicConfig(filename=log_file, format=log_format, level=INFO, datefmt=date_format)

_gemini_client = GeminiClient("https://jobcoin.gemini.com/viewing-hangup/api")

getcontext().prec = 15


async def main():
    house_address = create_address()
    # TODO: Allow configuration.
    config = MixerConfig(3.0, 10.0, 3)
    mixer = Mixer(_gemini_client, spread_evenly, house_address, config)
    while True:
        destination_addresses = await get_user_addresses()
        deposit_address = create_address()
        mix = PendingDepositMix(destination_addresses, deposit_address)
        await aprint(
            f"Thank you for submitting your destination addresses {destination_addresses}! You may "
            f"now send your jobcoins to the deposit address {deposit_address}."
        )
        mixer.watch(mix)


if __name__ == "__main__":
    asyncio.run(main())

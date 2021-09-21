import asyncio
from decimal import Decimal
from unittest.mock import MagicMock, AsyncMock, call

import pytest

from taurus.config import MixerConfig
from taurus.domain import Address, PendingDepositMix, PendingSettlementMix
from taurus.gemini_client import GeminiClient
from taurus.mixer import Mixer
from taurus.spreaders import spread_evenly


@pytest.fixture
def gemini_client():
    return MagicMock(spec=GeminiClient)


@pytest.fixture
@pytest.mark.asyncio
async def mixer(gemini_client):
    config = MixerConfig(0.0, 0.0, 3)
    mixer = Mixer(gemini_client, spread_evenly, Address("house"), config)
    yield mixer
    mixer.stop()


@pytest.mark.asyncio
async def test_start_mixing_settles_on_reaching_pending_floor(mixer: Mixer):
    mixer._settle = AsyncMock()
    mixer._pending_mixes = [1, 2, 3]
    await asyncio.sleep(0)
    mixer._settle.assert_called()


@pytest.mark.asyncio
async def test_start_mixing_does_not_settle_below_pending_floor(mixer: Mixer):
    mixer._settle = AsyncMock()
    await asyncio.sleep(0)
    mixer._settle.assert_not_called()


@pytest.mark.asyncio
async def test_watch_polls_deposit_address(gemini_client, mixer: Mixer):
    mix = PendingDepositMix([], Address("deposit"))
    balance = MagicMock()
    balance.json.return_value = {"balance": "0.1"}
    gemini_client.address_info = AsyncMock(return_value=balance)
    mixer.watch(mix)
    await asyncio.sleep(0)
    gemini_client.address_info.assert_called_with("deposit")


@pytest.mark.asyncio
async def test_watch_sends_jobcoins_when_deposit_detected(gemini_client, mixer: Mixer):
    mix = PendingDepositMix([Address("destination")], Address("deposit"))
    balance = MagicMock()
    balance.json.return_value = {"balance": "0.1"}
    gemini_client.address_info = AsyncMock(return_value=balance)
    mixer.watch(mix)
    await asyncio.sleep(0)
    gemini_client.send_jobcoins.assert_called_with(Address("deposit"), Address("house"), "0.1")


@pytest.mark.asyncio
async def test_settle_uses_spreader(mixer: Mixer):
    mixer._pending_mixes = [1, 2, 3]
    mixer._spreader = MagicMock()
    await mixer._settle()
    assert mixer._spreader.call_args_list == [call(1), call(2), call(3)]


@pytest.mark.asyncio
async def test_settle_sends_transactions(gemini_client, mixer: Mixer):
    mixer._pending_mixes = [
        PendingSettlementMix(
            [Address("destination_a"), Address("destination_b")],
            Address("deposit_a"),
            Decimal("1"),
        ),
        PendingSettlementMix([Address("destination_c")], Address("deposit_b"), Decimal("1")),
    ]
    await mixer._settle()
    await asyncio.sleep(0)
    assert gemini_client.send_jobcoins.call_args_list == [
        call("house", "destination_a", "0.5"),
        call("house", "destination_b", "0.5"),
        call("house", "destination_c", "1"),
    ]


@pytest.mark.asyncio
async def test_settle_clears_pending(mixer: Mixer):
    mixer._pending_mixes = [
        PendingSettlementMix(
            [Address("destination_a"), Address("destination_b")],
            Address("deposit_a"),
            Decimal("1"),
        ),
        PendingSettlementMix([Address("destination_c")], Address("deposit_b"), Decimal("1")),
    ]
    await mixer._settle()
    assert not mixer._pending_mixes

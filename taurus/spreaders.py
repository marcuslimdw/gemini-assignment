from decimal import getcontext
from typing import Callable

from taurus.domain import MixTransaction, PendingSettlementMix

getcontext().prec = 15

Spreader = Callable[[PendingSettlementMix], list[MixTransaction]]


def spread_evenly(mix: PendingSettlementMix) -> list[MixTransaction]:
    individual_amount = mix.amount / len(mix.user_addresses)
    return [MixTransaction(address, individual_amount) for address in mix.user_addresses]

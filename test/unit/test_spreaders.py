from decimal import Decimal

from taurus.spreaders import spread_evenly
from taurus.domain import PendingSettlementMix, Address, MixTransaction


def test_spread_evenly_exact():
    addresses = [Address("a"), Address("b")]
    mix = PendingSettlementMix(addresses, Address(""), Decimal("1"))
    actual = spread_evenly(mix)
    expected = [
        MixTransaction(Address("a"), Decimal("0.5")),
        MixTransaction(Address("b"), Decimal("0.5")),
    ]
    assert actual == expected


def test_spread_evenly_repeating_fraction():
    addresses = [Address("a"), Address("b"), Address("c")]
    mix = PendingSettlementMix(addresses, Address(""), Decimal("1"))
    actual = spread_evenly(mix)
    expected = [
        MixTransaction(Address("a"), Decimal("0.333333333333333")),
        MixTransaction(Address("b"), Decimal("0.333333333333333")),
        MixTransaction(Address("c"), Decimal("0.333333333333333")),
    ]
    assert actual == expected

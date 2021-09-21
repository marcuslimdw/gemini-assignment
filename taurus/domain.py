from dataclasses import dataclass
from decimal import Decimal
from typing import NewType

Address = NewType("Address", str)


@dataclass(frozen=True)
class PendingDepositMix:
    user_addresses: list[Address]
    deposit_address: Address


@dataclass(frozen=True)
class PendingSettlementMix:
    user_addresses: list[Address]
    deposit_address: Address
    amount: Decimal


@dataclass(frozen=True)
class MixTransaction:
    deposit_address: Address
    amount: Decimal

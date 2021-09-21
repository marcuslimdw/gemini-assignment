from typing import cast
from uuid import uuid4

from taurus.domain import Address
from taurus.exception import InvalidAddressEntered, NoAddressesEntered


def create_address() -> Address:
    return Address(uuid4().hex)


def parse_addresses(user_input: str) -> list[Address]:
    stripped = user_input.strip()
    if not stripped:
        raise NoAddressesEntered()

    addresses = stripped.split(",")
    for address in addresses:
        if not validate_address(address):
            raise InvalidAddressEntered(address)

    return cast(list[Address], addresses)


def validate_address(address: str) -> bool:
    return len(address) == 32 and set(address) <= set("abcdef1234567890")

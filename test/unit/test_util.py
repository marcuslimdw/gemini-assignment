import pytest

from taurus.domain import Address
from taurus.exception import NoAddressesEntered, InvalidAddressEntered
from taurus.util import validate_address, parse_addresses


def test_parse_addresses_success():
    user_input = "abcdef1234567890abcdef1234567890,1234567890abcdef1234567890abcdef"
    actual = parse_addresses(user_input)
    assert actual == [
        Address("abcdef1234567890abcdef1234567890"),
        Address("1234567890abcdef1234567890abcdef"),
    ]


def test_parse_addresses_no_address_failure():
    user_input = ""
    with pytest.raises(NoAddressesEntered):
        parse_addresses(user_input)


def test_parse_addresses_invalid_address_failure():
    user_input = "abcdef1234567890abcdef1234567890,invalid"
    with pytest.raises(InvalidAddressEntered) as exc_info:
        parse_addresses(user_input)

    assert exc_info.value.args[0] == "invalid"


@pytest.mark.parametrize(
    ["address", "expected"],
    [
        ("abcdef1234567890abcdef1234567890", True),
        ("abcdefghijklmnopqrstuvwxyz123456", False),
        ("short", False),
    ],
)
def test_validate_address(address: Address, expected: bool):
    assert validate_address(address) is expected

from aioconsole import ainput, aprint

from taurus.domain import Address
from taurus.exception import NoAddressesEntered, InvalidAddressEntered
from taurus.util import parse_addresses


async def get_user_addresses() -> list[Address]:
    while True:
        user_input = await ainput("Please enter a comma-separated list of addresses you own.\n")
        try:
            addresses = parse_addresses(user_input)

        except NoAddressesEntered:
            await aprint(f"Error: No addresses were entered. Please try again.")

        except InvalidAddressEntered as exc:
            await aprint(f"Error: {exc.args[0]} is an invalid Jobcoin address. Please try again.")

        else:
            return addresses

import pytest
from httpx import codes

from taurus.gemini_client import GeminiClient
from taurus.util import create_address


@pytest.fixture
def client():
    return GeminiClient("https://jobcoin.gemini.com/viewing-hangup/api")


@pytest.fixture
async def addresses():
    # If there was an API to create coins, we could create a balance in a testing account here.
    pass


@pytest.mark.asyncio
async def test_address_info(client):
    response = await client.address_info(create_address())
    assert response.status_code == codes.OK
    assert {"balance", "transactions"} == response.json().keys()


@pytest.mark.asyncio
async def test_global_history(client):
    response = await client.global_history()
    assert response.status_code == codes.OK


@pytest.mark.asyncio
async def test_send_jobcoins(client, addresses):
    response = await client.send_jobcoins(create_address(), create_address(), "0.01")
    # TODO: Set up fixture and assert on response.
    assert response.status_code in {codes.OK, codes.UNPROCESSABLE_ENTITY}

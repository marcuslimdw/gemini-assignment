from httpx import AsyncClient, Response

from taurus.domain import Address


# TODO: Add method for creating Jobcoins (which is not exposed in the API documentation, but can be seen from the web portal)


class GeminiClient:
    def __init__(self, base_url: str):
        self._base_url = base_url

    async def address_info(self, address: Address) -> Response:
        url = f"{self._base_url}/addresses/{address}"
        async with AsyncClient() as client:
            return await client.get(url)

    async def global_history(self) -> Response:
        url = f"{self._base_url}/transactions"
        async with AsyncClient() as client:
            return await client.get(url)

    async def send_jobcoins(self, from_address: Address, to_address: Address, amount: str) -> Response:
        url = f"{self._base_url}/transactions"
        body = {"fromAddress": from_address, "toAddress": to_address, "amount": amount}
        async with AsyncClient() as client:
            return await client.post(url, json=body)

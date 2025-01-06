import httpx
from api_client.client import Client
from api_client.dto.account_dto import BybitAccountDto


def account_info(database_id: int):
    response = Client.account_info(database_id)
    return BybitAccountDto(response)

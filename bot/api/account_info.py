import httpx
from api_client.client import Client
from api_client.dto.account_dto import AccountDto


def account_info(database_id: int) -> AccountDto:
    response = Client.account_info(database_id)
    account = AccountDto(response)

    return account

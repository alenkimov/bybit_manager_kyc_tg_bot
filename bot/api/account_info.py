import httpx
from APIClient.client import Client
from APIClient.dto.account_dto import AccountDto


def account_info(database_id: int) -> AccountDto:
    response = Client.account_info(database_id)
    account = AccountDto(response)

    return account

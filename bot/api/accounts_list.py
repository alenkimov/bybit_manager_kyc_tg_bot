from api_client.client import Client
from api_client.dto.database_account_dto import DatabaseAccountDto


def accounts_by_tg_provider(username: str):
    response = Client.accounts_by_provider(username=username)

    accounts = list(map(DatabaseAccountDto, response))

    return accounts

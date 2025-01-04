from api_client.client import Client
from api_client.dto.accounts_by_telegram_dto import AccountByKycProviderDto


def accounts_by_tg_provider(username: str):
    response = Client.accounts_by_provider(username=username)

    accounts = list(map(AccountByKycProviderDto, response))

    return accounts

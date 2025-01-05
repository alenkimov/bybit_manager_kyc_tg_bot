from bot.api.accounts_list import accounts_by_tg_provider
from api_client.dto.database_account_dto import DatabaseAccountDto


def get_accounts_by_provider(telegram_username: str) -> list[DatabaseAccountDto]:
    accounts: list[DatabaseAccountDto] = accounts_by_tg_provider(telegram_username)
    return [account for account in accounts if account.is_kyc_allowed()]

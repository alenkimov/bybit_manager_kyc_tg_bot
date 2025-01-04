from bot.api.accounts_list import accounts_by_tg_provider
from api_client.dto.accounts_by_telegram_dto import AccountByKycProviderDto


def get_accounts_by_provider(telegram_username: str) -> list[AccountByKycProviderDto]:
    accounts: list[AccountByKycProviderDto] = accounts_by_tg_provider(telegram_username)

    def check_account(account: AccountByKycProviderDto):
        return account.is_kyc_allowed()

    allowed_to_kyc = list(filter(check_account, accounts))

    return allowed_to_kyc

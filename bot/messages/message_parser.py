from bot.utils.time_diff import time_diff

from api_client.dto.account_dto import AccountDto
from api_client.dto.database_account_dto import DatabaseAccountDto
from api_client.dto.sumsub_url_dto import SumsubUrlDto


def stringify_message(
    account: AccountDto | DatabaseAccountDto, sumsub_url: SumsubUrlDto
):
    minutes, seconds = time_diff(sumsub_url.get_expiration_date())

    if minutes < 0 or seconds < 0:
        return (
            f"<b>{account.get_id()}</b> <code>{sumsub_url.get_url()}</code>\n\n"
            f"   EXPIRED"
        )

    return (
        f"<b>{account.get_id()}</b> <code>{sumsub_url.get_url()}</code>\n\n"
        f"⏱️{minutes:02}m{seconds:02}s | {account.get_status()}"
    )


def stringify_notallow_message(account: AccountDto | DatabaseAccountDto):
    return f"<b>{account.get_id()}</b>\n\n" f"{account.get_status()}"

import string
from bot.utils.time_diff import time_diff

from api_client.dto.account_dto import AccountDto
from api_client.dto.sumsub_url_dto import SumsubUrlDto


def stringify_message(account: AccountDto, sumsub_url: SumsubUrlDto | None = None):

    if not account.is_kyc_allowed() or not sumsub_url:
        return stringify_notallow_message(account.get_id(), account.get_status())

    minutes, seconds = time_diff(sumsub_url.get_expiration_date())

    if minutes < 0 or seconds < 0:
        return stringify_expired_link(account.get_id(), sumsub_url.get_url())

    return stringify_url_message(
        account.get_id(), account.get_status(), sumsub_url.get_url(), minutes, seconds
    )


def stringify_url_message(
    database_id: int, status: str, url: str, minutes: int, seconds: int
):
    return (
        f"<b>{database_id}</b> <code>{url}</code>\n\n"
        f"⏱️{minutes:02}m{seconds:02}s | {status}"
    )


def stringify_expired_link(database_id: int, url: str):
    return f"<b>{database_id}</b> <code>{url}</code>\n\n" f"   EXPIRED"


def stringify_notallow_message(databasse_id: int, status: str):
    return f"<b>{databasse_id}</b>\n\n" f"{status}"

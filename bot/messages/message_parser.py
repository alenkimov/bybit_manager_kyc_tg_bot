from bot.utils.time_diff import time_diff
from APIClient.dto.account_dto import AccountDto


def stringify_message(account: AccountDto, link):
    minutes, seconds = time_diff(link["expired_at"])

    if minutes < 0 or seconds < 0:
        return (
            f"<b>{account.get_id()}</b> <code>{link["kyc_url"]}</code>\n\n"
            f"   EXPIRED"
        )

    return (
        f"<b>{account.get_id()}</b> <code>{link["kyc_url"]}</code>\n\n"
        f"⏱️{minutes:02}m{seconds:02}s | {account.get_status()}"
    )


def stringify_notallow_message(account: AccountDto):
    return f"<b>{account.get_id()}</b>\n\n" f"{account.get_status()}"

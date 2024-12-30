from bot.utils.time_diff import time_diff


def stringify_message(account, link):
    minutes, seconds = time_diff(link["expired_at"])

    if minutes < 0 or seconds < 0:
        return (
            f"<b>{account["database_id"]}</b> <code>{link["kyc_url"]}</code>\n\n"
            f"   EXPIRED"
        )

    return (
        f"<b>{account["database_id"]}</b> <code>{link["kyc_url"]}</code>\n\n"
        f"⏱️{minutes:02}m{seconds:02}s | {account['kyc']['state'][0]['status']}"
    )


def stringify_notallow_message(account):
    return (
        f"<b>{account['database_id']}</b>\n\n" f"{account['kyc']['state'][0]['status']}"
    )
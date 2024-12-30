from bot.api.accounts_list import ids_by_tg_provider
from bot.api.server_config import get_endpoint
from bot.api.account_info import account_info


def get_accounts_by_provider(username):
    ids = ids_by_tg_provider(username)
    accounts = []
    for id in ids:
        account = account_info(id)
        if account["kyc"]["state"][0]["status"] == "ALLOW":
            accounts.append(account)
    return accounts

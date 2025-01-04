import httpx
from api_client.client import Client
from api_client.dto.account_dto import AccountDto


def account_info(id) -> AccountDto:
    response = Client.account_info(id)
    account = AccountDto(response)

    # response = httpx.post(get_endpoint("accInfo", id=id))
    # if response.status_code != httpx.codes.OK:
    #     raise Exception("Error while getting account" + id)
    # info = response.json()

    # if not "database_id" in info:  # Изменилась схема
    #     info["database_id"] = id
    # return info

    return account

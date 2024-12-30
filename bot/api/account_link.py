import httpx
from bot.api.server_config import get_endpoint


def account_link(id):
    response = httpx.post(get_endpoint("accLink", id=id))
    if response.status_code != httpx.codes.OK:
        raise Exception("Error while getting account" + id)
    info = response.json()
    return info

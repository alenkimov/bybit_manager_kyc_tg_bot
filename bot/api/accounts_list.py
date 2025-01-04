import httpx
from bot.api.server_config import get_endpoint


def ids_by_tg_provider(username: str):
    response = httpx.get(get_endpoint("IdsByProvider", nickname=username))
    if response.status_code != httpx.codes.OK:
        raise Exception(f"Error while getting accounts! Status code {response.status_code}")
    ids = response.json()

    if "database_ids" not in ids:
        raise KeyError("Key 'database_ids' not found in response")
    return ids["database_ids"]

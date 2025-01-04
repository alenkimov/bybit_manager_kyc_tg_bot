import httpx
from APIClient.client import Client
from bot.api.server_config import get_endpoint


def account_link(database_id: int):
    response = Client.account_link(database_id)
    return response

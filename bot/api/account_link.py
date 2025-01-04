from api_client.dto.sumsub_url_dto import SumsubUrlDto
from api_client.client import Client


def account_link(database_id: int):
    response = Client.account_link(database_id)
    return SumsubUrlDto(response)

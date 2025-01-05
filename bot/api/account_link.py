from api_client.dto.sumsub_url_dto import SumsubUrlDto
from api_client.client import Client


def account_sumsub_url(database_id: int):
    response = Client.subsub_url(database_id)
    return SumsubUrlDto(response)

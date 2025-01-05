from typing import TypedDict

from api_client.dto.database_account_dto import DatabaseAccountDto
from api_client.dto.sumsub_url_dto import SumsubUrlDto

chat_data = {}


class AccountData(TypedDict):
    account: DatabaseAccountDto
    link: SumsubUrlDto | None


class ChatDataEntry(TypedDict):
    """
    accounts: {database_id: {account, link}}
    bad: [database_id]
    delayed: {database_id: timestamp}
    """

    accounts: dict[str, AccountData]
    bad: list[str]
    delayed: dict[str, float]


ChatData = list[tuple[str, ChatDataEntry]]

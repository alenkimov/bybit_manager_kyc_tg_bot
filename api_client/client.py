from os import access
import httpx
from .dto.account_dto import AccountDto
from .dto.sumsub_url_dto import SumsubUrlDto

BASE_URL = "http://127.0.0.1:8000/"

ENDPOINTS = {
    "accounts_by_provider": "get_accounts/{telegram_username}",
    "account_info": "private/{database_id}/kyc_info?obtain_current=false&obtain_kyc_token=false&obtain_quotas=false&obtain_state=true&obtain_verification_process=false&obtain_aml_questionnaire=true&submit_kyc_questionnaire=true&set_kyc_complete_time=false",
    "sumsub_link": "private/{database_id}/sumsub_kyc_url",
}

# A client with a 60s timeout for connecting, and a 10s timeout elsewhere.
timeout = httpx.Timeout(10.0, connect=60.0)
client = httpx.Client(timeout=timeout)


def get_endpoint(key, **kwargs):
    endpoint = ENDPOINTS.get(key)
    if not endpoint:
        raise ValueError(f"Endpoint '{key}' does not exist.")
    return endpoint.format(**kwargs)


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url or BASE_URL

    def _request(self, method: str, url: str, **kwargs) -> str | dict | list:
        response = client.request(method, url, **kwargs)
        if response.status_code != httpx.codes.OK:
            raise Exception(f"API Error: {response.status_code}, {response.text}")

        return response.json()

    def post(self, url: str, **kwargs):
        return self._request("POST", url, **kwargs)

    def get(self, url: str, **kwargs):
        return self._request("GET", url, **kwargs)

    def accounts_by_provider(self, username: str):
        url = self.base_url + get_endpoint(
            "accounts_by_provider", telegram_username=username
        )
        response = self.get(url)
        return response

    def account_info(self, database_id: int):
        url = self.base_url + get_endpoint("account_info", database_id=database_id)
        response = self.post(url)

        # Норм решение?
        response["database_id"] = database_id  # type: ignore

        return response

    def subsub_url(self, databse_id: int):
        url = self.base_url + get_endpoint("sumsub_link", database_id=databse_id)
        response = self.post(url)

        return response


Client = APIClient(BASE_URL)

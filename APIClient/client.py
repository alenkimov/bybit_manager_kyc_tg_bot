import httpx

BASE_URL = "http://127.0.0.1:8000/"

ENDPOINTS = {
    "ids_by_provider": "get_kyc_provider_database_ids/{nickname}",
    "account_info": "private/{id}/kyc_info?obtain_current=false&obtain_kyc_token=false&obtain_quotas=false&obtain_state=true&obtain_verification_process=false&obtain_aml_questionnaire=true&submit_kyc_questionnaire=true&set_kyc_complete_time=false",
    "sumsub_link": "private/{id}/sumsub_kyc_url",
}


def get_endpoint(key, **kwargs):
    endpoint = ENDPOINTS.get(key)
    if not endpoint:
        raise ValueError(f"Endpoint '{key}' does not exist.")
    return endpoint.format(**kwargs)


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url or BASE_URL

    def _request(self, url, method="GET", params=None, data=None):

        response = ""
        if method == "POST":
            response = httpx.post(url, params=params, data=data)
        else:
            response = httpx.get(url, params=params)

        if response.status_code != httpx.codes.OK:
            raise Exception(f"API Error: {response.status_code}, {response.text}")

        return response.json()

    def account_info(self, id: int):
        url = self.base_url + get_endpoint("account_info", id=id)
        response = self._request(url, method="POST")

        if not "database_id" in response:  # Изменилась схема
            response["database_id"] = id

        return response


Client = APIClient(BASE_URL)

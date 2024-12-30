BASE_URL = "http://127.0.0.1:8000/"

ENDPOINTS = {
    "IdsByProvider": "get_kyc_provider_database_ids/{nickname}",
    "accInfo": "private/{id}/kyc_info?obtain_current=false&obtain_kyc_token=false&obtain_quotas=false&obtain_state=true&obtain_verification_process=false&obtain_aml_questionnaire=true&submit_kyc_questionnaire=true&set_kyc_complete_time=false",
    "accLink": "private/{id}/sumsub_kyc_url",
}


def get_endpoint(key, **kwargs):
    endpoint = ENDPOINTS.get(key)
    if not endpoint:
        raise ValueError(f"Endpoint '{key}' does not exist.")
    return BASE_URL + endpoint.format(**kwargs)

import copy


class SumsubUrlDto:
    def __init__(self, api_link):
        self.data = copy.deepcopy(api_link)

    def get_url(self) -> str:
        return self.data["kyc_url"]

    def get_expiration_date(self) -> int:
        return self.data["expired_at"]

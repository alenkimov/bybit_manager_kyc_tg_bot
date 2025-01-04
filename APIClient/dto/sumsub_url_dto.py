import copy


class SumsubUrlDto:
    def __init__(self, apiLink):
        self.data = copy.deepcopy(apiLink)

    def get_link(self) -> str:
        return self.data.kyc_url

    def get_expiration_date(self) -> str:
        return self.data.expired_at

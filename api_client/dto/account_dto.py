import copy


class AccountDto:
    def __init__(self, apiAccount):
        self.data = copy.deepcopy(apiAccount)

    def get_status(self) -> str:
        return self.data["state"][0]["status"]

    def get_id(self) -> int:
        return self.data["database_id"]

    def set_status(self, status: str):
        self.data["state"][0]["status"] = status

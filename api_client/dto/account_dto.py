import copy


class AccountDto:
    def __init__(self, apiAccount):
        self.data = copy.deepcopy(apiAccount)

    def get_status(self) -> str:
        return self.data["state"][0]["status"]

    def is_kyc_allowed(self):
        return (
            self.get_status() == "ALLOW" or self.get_status() == "FAILED_AND_CAN_RETRY"
        )

    def get_id(self) -> int:
        return self.data["database_id"]

    def set_status(self, status: str):
        self.data["state"][0]["status"] = status

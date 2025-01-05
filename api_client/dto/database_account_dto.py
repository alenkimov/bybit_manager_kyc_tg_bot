import copy


class DatabaseAccountDto:
    def __init__(self, account):
        # TODO: Доделать норм схему
        self.data = copy.deepcopy(account)

    def get_status(self) -> str:
        return self.data["kyc_status"]

    def set_status(self, status: str):
        self.data["kyc_status"] = status

    def is_kyc_allowed(self):
        return (
            self.get_status() == "ALLOW" or self.get_status() == "FAILED_AND_CAN_RETRY"
        )

    def get_id(self) -> int:
        return self.data["database_id"]

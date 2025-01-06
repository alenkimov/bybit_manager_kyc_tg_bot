import copy
from abc import ABC, abstractmethod


class AccountDto(ABC):
    @abstractmethod
    def get_status(self) -> str:
        """
        Возвращает статус аккаунта.
        """
        pass

    @abstractmethod
    def set_status(self, status: str):
        """
        Устанавливает статус аккаунта.
        """
        pass

    @abstractmethod
    def get_id(self) -> int:
        """
        Возвращает идентификатор аккаунта.
        """
        pass

    def is_kyc_allowed(self) -> bool:
        """
        Проверяет, разрешён ли KYC для аккаунта.
        """
        return self.get_status() in {"ALLOW", "FAILED_AND_CAN_RETRY"}


class BybitAccountDto(AccountDto):
    def __init__(self, apiAccount):
        # TODO: Доделать норм схему
        self.data = copy.deepcopy(apiAccount)

    def get_status(self) -> str:
        return self.data["state"][0]["status"]

    def get_id(self) -> int:
        return self.data["database_id"]

    def set_status(self, status: str):
        self.data["state"][0]["status"] = status


class DatabaseAccountDto(AccountDto):
    def __init__(self, account):
        # TODO: Доделать норм схему
        self.data = copy.deepcopy(account)

    def get_status(self) -> str:
        return self.data["kyc_status"]

    def set_status(self, status: str):
        self.data["kyc_status"] = status

    def get_id(self) -> int:
        return self.data["database_id"]

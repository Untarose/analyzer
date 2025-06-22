from abc import ABC, abstractmethod
from interfaces.base_dataunit import BaseDataUnit

class BaseDataGroup(ABC):
    @property
    @abstractmethod
    def units(self) -> dict[str, BaseDataUnit]:
        """
        辞書型のDataUnitの一覧を返す
        """
        pass
    @abstractmethod
    def get_unit(self, unit_name: str) -> BaseDataUnit:
        """
        指定したnameをもつDataUnitを返す
        """
        pass
    @abstractmethod
    def exist_unit_name(self, unit_name: str) -> bool:
        """
        指定したnameをもつunitを持っているか
        """
        pass
    @abstractmethod
    def unit_names(self) -> list[str]:
        """
        unitsの名前列を返す
        """
        pass

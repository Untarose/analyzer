from abc import ABC, abstractmethod
from pathlib import Path
from interfaces.dataunit_interface import DataUnitInterface

class DataGroupInterface(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Groupの名前を返す
        """
    @property
    @abstractmethod
    def units(self) -> dict[str, DataUnitInterface]:
        """
        辞書型のDataUnitの一覧を返す
        """
        pass
    @property
    @abstractmethod
    def path(self) -> Path:
        """
        データが保存されている絶対pathを返す
        """
        pass
    @abstractmethod
    def get_unit(self, unit_name: str) -> DataUnitInterface:
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
    def add_unit(self, new_unit: DataUnitInterface) -> None:
        """
        # TODO テストへの追記
        DataGroupにUnitを追加する
        """
    @abstractmethod
    def with_update_name(self, new_name: str) -> "DataGroupInterface":
        """
        datagroupのmetaデータのnameを変更する
        """
        pass
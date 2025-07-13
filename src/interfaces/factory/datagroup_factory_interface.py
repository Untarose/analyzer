from abc import ABC, abstractmethod
from pathlib import Path
from interfaces.data_group.datagroup_interface import DataGroupInterface
from interfaces.data_unit.dataunit_interface  import DataUnitInterface
from interfaces.metas.meta_interface import MetaInterface
class DataGroupFactoryInterface(ABC):
    @abstractmethod
    def create(self, units: list[DataUnitInterface], name: str, path: Path) -> DataGroupInterface:
        """
        DataUnitの配列を用いてDataGroupのインスタンスを返す
        """
        pass
    @abstractmethod
    def _create_meta(self, name: str, path: Path) -> MetaInterface:
        """
        Metaを構築するメソッド
        """
        pass
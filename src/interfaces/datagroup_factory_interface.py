from abc import ABC, abstractmethod
from interfaces.datagroup_interface import DataGroupInterface
from interfaces.dataunit_interface  import DataUnitInterface

class DataGroupFactoryInterface(ABC):
    @abstractmethod
    def create(self, units: list[DataUnitInterface], name, path) -> DataGroupInterface:
        """
        DataUnitの配列を用いてDataGroupのインスタンスを返す
        """
        pass
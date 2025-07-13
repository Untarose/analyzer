
from abc import abstractmethod
from pathlib import Path
from typing import Generic, TypeVar
from pandas.core.api import DataFrame as DataFrame
from interfaces.factory.dataunit_factory_interface import DataUnitFactoryInterface
from interfaces.data_unit.dataunit_interface import DataUnitInterface
from cores.data_unit.dataunit import DataUnit
from cores.metas.dataunit_meta import DataUnitMeta

class BaseDataUnitFactory(DataUnitFactoryInterface):
    @abstractmethod
    def create(self, raw_data: object, name: str, path: Path) -> list[DataUnitInterface]:
        """
        すでに構造化したデータを読み込む、基本のDataUnit生成メソッド
        """
        raise NotImplementedError(f"{self.__class__.__name__}.create() is not implemented.")
        
    
    def _create_meta(self, name: str, path: Path) -> DataUnitMeta:
        return DataUnitMeta(name=name, path=path)

    
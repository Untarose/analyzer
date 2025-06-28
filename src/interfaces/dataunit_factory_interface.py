from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar
from pandas.core.api import DataFrame as DataFrame

from interfaces.data_repository import DataRepositoryInterface
from interfaces.dataunit_interface import DataUnitInterface
from interfaces.meta_interface import MetaInterface

class DataUnitFactoryInterface(ABC):
    @abstractmethod
    def create(self, raw_data: object, name: str, path: Path) -> DataUnitInterface:
        """
        基本のDataUnit生成メソッド
        """
        pass

    @abstractmethod
    def _create_meta(self, name: str, path: Path) -> MetaInterface:
        """
        Metaを構築するメソッド
        """
        pass
        
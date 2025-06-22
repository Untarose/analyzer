from abc import ABC, abstractmethod
from typing import Any
import pandas as pd

class DataUnitInterface(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """ユニット名を返す"""
        pass

    @property
    @abstractmethod
    def df(self) -> pd.DataFrame:
        """データ本体を返す"""
        pass

    @property
    @abstractmethod
    def metadata(self) -> dict[str, Any]:
        """メタ情報を返す"""
        pass
    @abstractmethod
    def with_updated_name(self, new_name: str) -> "DataUnitInterface":
        """名前を更新して新しいユニットを返す。immutable"""
        pass
    @abstractmethod
    def with_updated_df(self, new_df: pd.DataFrame) -> "DataUnitInterface":
        """新しいDataFrameで新しいユニットを返す。immutable"""
        pass
    @abstractmethod
    def with_update_metadata(self, key:str, value: Any) -> "DataUnitInterface":
        """メタ情報を更新して新しいユニットを返す。immutable"""
        pass


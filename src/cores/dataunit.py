
from typing import Any, Self
from pandas.core.api import DataFrame as DataFrame
from interfaces.dataunit_interface import DataUnitInterface

class DataUnit(DataUnitInterface):
    
    def __init__(self, name: str, df: DataFrame, metadata: dict[str, Any]) -> None:
        """
        DataUnitの初期化。空のnameやDataFrameは禁止
        """
        if not name:
            raise ValueError("name must not be empty")
        if df.empty:
            raise ValueError("df must not be empty")
        self._name = name
        self._df = df
        self._metadata = metadata

    @property
    def name(self) -> str:
        """
        getter ユニットの名前を返す
        """
        return self._name

    @property
    def df(self) -> DataFrame:
        """
        getter ユニットのDataFrameを返す
        """
        return self._df

    @property
    def metadata(self) -> dict[str, Any]:
        """
        getter ユニットのmetadataを返す
        """
        return self._metadata

    def with_updated_name(self, new_name: str) -> Self:
        """
        immutable setter 新しいユニット名をもった新規ユニットを返す
        """
        return self.__class__(new_name, self.df, self.metadata)

    def with_updated_df(self, new_df: DataFrame) -> Self:
        """
        immutable setter 新しいDataFrameをもった新規ユニットを返す 
        """
        return self.__class__(self.name, new_df, self.metadata)

    def with_update_metadata(self, key: str, value: Any) -> Self:
        """
        immutable setter 新しいメタデータを持った（更新した）新規ユニットを返す
        """
        new_metadata = self.metadata.copy()
        new_metadata[key] = value
        return self.__class__(self.name, self.df, new_metadata)

    

    
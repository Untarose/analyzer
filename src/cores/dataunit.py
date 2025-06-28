
from typing import Any, Self
from dataclasses import replace, asdict
from pandas.core.api import DataFrame as DataFrame
from interfaces.dataunit_interface import DataUnitInterface
from cores.metas.dataunit_meta import DataUnitMeta

class DataUnit(DataUnitInterface):
    
    def __init__(self, df: DataFrame, metadata: DataUnitMeta) -> None:
        """
        DataUnitの初期化。空のnameやDataFrameは禁止
        """
        if df.empty:
            raise ValueError("df must not be empty")
        self._df = df
        self._metadata = metadata

    @property
    def name(self) -> str:
        """
        getter ユニットの名前を返す
        """
        return self._metadata.name

    @property
    def df(self) -> DataFrame:
        """
        getter ユニットのDataFrameを返す
        """
        return self._df

    @property
    def metadata(self) -> DataUnitMeta:
        """
        getter ユニットのmetadataを返す
        """
        return self._metadata

    def with_updated_name(self, new_name: str) -> Self:
        """
        immutable setter 新しいユニット名をもった新規ユニットを返す
        """
        new_metadata = replace(self._metadata, name=new_name)
        return self.__class__(self.df, new_metadata)
    

    

    
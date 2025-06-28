
from typing import Any, Self
from dataclasses import replace, asdict
from datetime import datetime
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
        new_namedata = replace(new_metadata, created_at = datetime.now())
        return self.__class__(self.df, new_metadata)

    def with_updated_df(self, new_df: DataFrame) -> Self:
        """
        immutable setter 新しいDataFrameをもった新規ユニットを返す 
        """
        return self.__class__(new_df, self.metadata)

    def with_update_metadata(self, key: str, value: Any) -> Self:
        """
        immutable setter 新しいメタデータを持った（更新した）新規ユニットを返す
        いらないかもpendings
        """
        if not hasattr(self._metadata, key):
            raise AttributeError('metadata objects dont have "{key}" field')
        # asdictを用いてmetadataを辞書型に変換
        metadata_dict = asdict(self._metadata)
        
        metadata_dict[key] = value
        new_metadata = self._metadata.__class__(**metadata_dict)
        return self.__class__(self.df, new_metadata)

    

    
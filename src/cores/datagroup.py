from dataclasses import replace, asdict
from pathlib import Path
from collections.abc import Mapping
from interfaces.datagroup_interface import DataGroupInterface
from interfaces.dataunit_interface import DataUnitInterface
from cores.metas.datagroup_meta import DataGroupMeta
class DataGroup(DataGroupInterface):

    def __init__(self,units: Mapping[str, DataUnitInterface], meta: DataGroupMeta) -> None:
        self._units = dict(units)
        self._metadata = meta
        

    @property
    def name(self) -> str:
        return self._metadata.name

    @property
    def path(self) -> Path:
        return self._metadata.path
    
    @property
    def units(self) -> dict[str, DataUnitInterface]:
        """
        辞書型のDataUnitの一覧を返す
        """
        return self._units

    def get_unit(self, unit_name: str) -> DataUnitInterface:
        """
        指定したnameをもつDataUnitを返す
        """
        if self.exist_unit_name(unit_name):
            return self.units[unit_name]
        else:
            raise ValueError(f'your specified {unit_name} is not exist')

    def exist_unit_name(self, unit_name: str) -> bool:
        """
        指定したnameをもつunitを持っているか
        """
        return unit_name in self.unit_names()
    
    def add_unit(self, new_unit: DataUnitInterface) -> None:
        """
        # TODO テストへの追記
        DataGroupにUnitを追加する
        """
        self._units[new_unit.name] = new_unit

    def unit_names(self) -> list[str]:
        """
        unitsの名前列を返す
        """
        return list(self._units.keys())

    def with_update_name(self, new_name: str) -> DataGroupInterface:
        """
        metaの中のnameを変更する
        """
        new_metadata = replace(self._metadata, name=new_name)
        return self.__class__(self._units, new_metadata)
    
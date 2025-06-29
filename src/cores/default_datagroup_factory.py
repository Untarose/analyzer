from pathlib import Path
from interfaces.datagroup_interface import DataGroupInterface
from interfaces.dataunit_interface  import DataUnitInterface
from interfaces.datagroup_factory_interface import DataGroupFactoryInterface
from cores.metas.datagroup_meta import DataGroupMeta
from cores.datagroup import DataGroup

class DefaultDataGroupFactory(DataGroupFactoryInterface):
    def create(self, units: list[DataUnitInterface], name, path) -> DataGroupInterface:
        """
        DataUnitの配列を用いてDataGroupのインスタンスを返す
        """
        data_group_meta = self._create_meta(name=name, path=path)
        units_dict = {
            unit.name: unit for unit in units
        }
        return DataGroup(units_dict, data_group_meta)
    def _create_meta(self, name: str, path: Path) -> DataGroupMeta:
        """
        name, pathからDataGroupMetaクラスを作成する
        """
        return DataGroupMeta(name, path)
from pandas import DataFrame
from pathlib import Path
from interfaces.builder.data_builder_interface import DataBuilderInterface
from interfaces.data_group.datagroup_interface import DataGroupInterface
from interfaces.factory.dataunit_factory_interface import DataUnitFactoryInterface
from interfaces.factory.datagroup_factory_interface import DataGroupFactoryInterface
class DataBuilder(DataBuilderInterface):
    def __init__(self, dataunit_factory: DataUnitFactoryInterface, datagroup_factory: DataGroupFactoryInterface) -> None:
        self._dataunit_factory = dataunit_factory
        self._datagroup_factory = datagroup_factory
    def group_to_dict(self, groups: list[DataGroupInterface], units_selection: dict[str, list[str]]) -> dict[str, dict[str, DataFrame]]:
        arguments = {}
        for group in groups:
            group_name = group.name
            arguments[group_name] = {}
            unit_names = units_selection.get(group_name, [])
            # unit_namesが空ならgroupに格納されたすべてのunitを取得
            target_names = unit_names or group.unit_names()
            for unit_name in target_names:
                unit = group.get_unit(unit_name=unit_name)
                arguments[group_name][unit_name] = unit.df
        return arguments

    def dict_to_group(self, groups_dict: dict[str, dict[str, DataFrame]], parent_path: Path) -> list[DataGroupInterface]:
        groups = []
        for group_name, units_data in groups_dict.items():
            group_path = parent_path / group_name
            units = []
            for unit_name, unit_df in units_data.items():
                unit_path = group_path / unit_name
                units.extend(
                    self._dataunit_factory.create(unit_df, unit_name, unit_path)
                )
            groups.append(
                self._datagroup_factory.create(units, group_name, group_path)
            )
        return groups
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
    def group_to_dict(self, groups: list[DataGroupInterface], units_selection: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, DataFrame]]:
        """
        - units_selectionの構造:
            引数名（関数の引数）: {
                グループ名: [ユニット名1, ユニット名2, ...]
            }

        - 戻り値:
            引数名: {
                ユニット名: DataFrame
            }
        """
        # DataGroupの名前からオブジェクトを逆引きできるように
        group_map = {group.name: group for group in groups}
        arguments = {}

        for arg_name, group_to_units in units_selection.items():
            arg_units: dict[str, DataFrame] = {}

            for group_name, unit_names in group_to_units.items():
                if group_name not in group_map:
                    raise ValueError(f"group_to_dict: 指定されたグループ名 '{group_name}' は存在しません。")

                group = group_map[group_name]
                target_unit_names = unit_names or group.unit_names()

                for unit_name in target_unit_names:
                    if not group.exist_unit_name(unit_name):
                        raise ValueError(f"group_to_dict: グループ '{group_name}' にユニット '{unit_name}' は存在しません。")
                    unit = group.get_unit(unit_name=unit_name)
                    arg_units[unit_name] = unit.df

            arguments[arg_name] = arg_units

        return arguments

    def dict_to_group(self, groups_dict: dict[str, dict[str, DataFrame]], parent_path: Path) -> list[DataGroupInterface]:
        groups = []
        for group_name, units_data in groups_dict.items():
            group_path = parent_path / group_name
            units = []
            for unit_name, unit_df in units_data.items():
                unit_path = (group_path / '__DATA__') / unit_name
                units.extend(
                    self._dataunit_factory.create(unit_df, unit_name, unit_path)
                )
            groups.append(
                self._datagroup_factory.create(units, group_name, group_path)
            )
        return groups
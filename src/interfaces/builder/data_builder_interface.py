from abc import ABC, abstractmethod
from pathlib import Path
from pandas import DataFrame

from interfaces.data_group.datagroup_interface import DataGroupInterface


class DataBuilderInterface(ABC):
    @abstractmethod
    def group_to_dict(self, groups: list[DataGroupInterface], units_selection: dict[str, list[str]]) -> dict[str, dict[str, DataFrame]]:
        """関数で処理するGroupをDictに変換するメソッド

        Args:
            group (DataGroupInterface): Analyzerで渡されるDataGroup
            units_selection (dict[str, list[str]]): ユーザーから渡されたExecContext内のunits_selectionをAnalyzerから渡される

        Returns:
            dict[str, dict[str, DataFrame]]: 関数で使われる引数を返す
        """
    @abstractmethod
    def dict_to_group(self, groups_dict :dict[str, dict[str, DataFrame]], parent_path: Path) -> list[DataGroupInterface]:
        """関数の返り値をGroupに変換する

        Args:
            group_dict (dict[str, dict[str, DataFrame]]): Analyzerに格納するGroupを追加
        """
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from pandas import DataFrame

from cores.exec_context import ExecContext
from interfaces.datagroup_interface import DataGroupInterface
class ExecutorInterface(ABC):
    @abstractmethod
    def exec(self, executor_context: ExecContext, groups: list[DataGroupInterface]) -> list[DataGroupInterface]:
        """
        groupの指定したunit_names (Noneならすべて)に対して
        funcを行った結果のdict[group_name, dict[unit_name, DataFrame]] を返す
        """
        pass
    @abstractmethod
    def _create_common_group_path(self, groups: list[DataGroupInterface]) -> Path:
        """
        使用するgroupのパスの共通部分のパスを返す
        """
        pass
    @abstractmethod
    def _is_expext_result(self, result: object) -> bool:
        """
        funcの実行結果が正しいかどうか
        """
        pass
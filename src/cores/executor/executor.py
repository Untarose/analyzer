from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Callable
from pandas import DataFrame
import os

from cores.executor.exec_context import ExecContext
from interfaces.executor.executor_interface import ExecutorInterface
from interfaces.builder.data_builder_interface import DataBuilderInterface
from interfaces.data_group.datagroup_interface import DataGroupInterface
from interfaces.data_unit.dataunit_interface import DataUnitInterface

class Executor(ExecutorInterface):
    def __init__(self, data_builder: DataBuilderInterface) -> None:
        self._data_builder = data_builder
        
    def exec(self, executor_context: ExecContext, groups: list[DataGroupInterface]) -> list[DataGroupInterface]:
        func = executor_context.func
        # funcの引数用のデータ作成
        groups_arguments = self._data_builder.group_to_dict(
            groups=groups,
            units_selection=executor_context.units_selection
        )
        # 関数実行
        result = func(**groups_arguments, **executor_context.kwargs)
        # dict[str, dict[str, DataFrame]]でないなら空のリストを返す
        if not self._is_expext_result(result=result):
            return []
        # groupのpathは，使用したgroupのpath共通部分
        common_path = self._create_common_group_path(groups=groups)
        # analyzer格納用データ作成
        result_groups = self._data_builder.dict_to_group(
            groups_dict=result,
            parent_path=common_path
        )
        
        return result_groups

    def _create_common_group_path(self, groups: list[DataGroupInterface]) -> Path:
        common_path = Path(
                os.path.commonpath(
                    [ str(group.path) for group in groups ]
            )
        )
        
        return common_path
    
    def _is_expext_result(self, result: object) -> bool:
        if not isinstance(result, dict):
            print(f"{self.__class__}: some groups is not dict. so all new groups didn't created. Just only Execute your function.")
            return False
        for group_name, unit_dict in result.items():
            if not isinstance(unit_dict, dict):
                print(f"{self.__class__}: some units is not dict. so all new groups didn't created. Just only Execute your function.")
                return False
            for unit_name, df in unit_dict.items():
                if not isinstance(df, DataFrame):
                    print(f"{self.__class__}: some dfs is not Data. so all new groups didn't created. Just only Execute your function.")
                    return False
        return True
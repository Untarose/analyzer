from dataclasses import dataclass, field
from typing import Callable, Optional, Mapping
import inspect

from interfaces.data_group.datagroup_interface import DataGroupInterface
@dataclass
class ExecContext:
    func: Callable
    units_selection : dict[str, dict[str, list[str]]]
    kwargs: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self):
        """コンストラクタ作成時に呼び出される
        """
        self._validation_func_args()

    def _validation_func_args(self):
        """コンストラクトされたときに呼び出される。
           関数funcの引数名と、指定したunits_selection, kwargsに指定したkey名が一致するかどうか
           これは、ユーザにGroup、Unitを操作する際の関数と指定したGroup、Unitの明示を強要する。

        Raises:
            ValueError: 関数funcに**kwargsを使用することはできない
        """
        sig = inspect.signature(self.func)

        # **kwargs を禁止
        if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in sig.parameters.values()):
            raise ValueError("関数に **kwargs を含めることはできません。明示的に全ての引数を定義してください。")

        # 関数の全引数名
        func_args = list(sig.parameters.keys())

        # ExecContext で指定された全引数名
        context_args = list(self.units_selection.keys()) + list(self.kwargs.keys())

        # 不足・余剰チェック
        missing = [arg for arg in func_args if arg not in context_args]
        extra = [key for key in context_args if key not in func_args]

        if missing or extra:
            msg = ""
            if missing:
                msg += f"関数の引数 {missing} が ExecContext に存在しません。\n"
            if extra:
                msg += f"ExecContext に余計な引数 {extra} が存在します。\n"
            raise ValueError(f"ExecContext の検証に失敗しました:\n{msg}")
        else:
            print('✅ ExecContext: 引数の整合性チェックOK')
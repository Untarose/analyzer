from abc import ABC, abstractmethod
from pathlib import Path
from interfaces.data_group.datagroup_interface import DataGroupInterface
from cores.executor.exec_context import ExecContext
class AnalyzerInterface(ABC):
    @property
    @abstractmethod
    def root_directory(self) -> Path:
        """
        rootディレクトリを返す
        """
        pass
    @abstractmethod
    def group_names(self) -> list[str]:
        """
        groupsの名前のリストを返す
        """
        pass

    @abstractmethod
    def delete_group(self, group_name: str) -> None:
        """
        指定した名前のグループをgroupsから消す
        """
        pass

    @abstractmethod
    def exist_group_name(self, group_name: str) -> bool:
        """
        指定したグループ名が存在するかどうかを返す
        """
        pass
    @abstractmethod
    def save_group(self, group_name: str) -> None:
        """
        指定したグループをファイルに保存する
        """
        pass
    @abstractmethod
    def run(self, exec_context: ExecContext) -> None:
        """
        関数を実行する
        関数での返り値が指定されたものであれば，その結果を新しいグループとして登録する．
        ただし，すでに新しいグループが登録されている場合，すべての新しいグループは登録されない
        """
        pass




from abc import ABC, abstractmethod
from pathlib import Path
from cores.datagroup import DataGroup
class BaseAnalyzer(ABC):
    @property
    @abstractmethod
    def root_directory(self) -> Path:
        """
        データのrootディレクトリを返す
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
    def get_group(self, group_name: str) -> DataGroup:
        """
        指定した名前のグループを返す
        """
        pass

    @abstractmethod
    def _add_group(self, new_group: DataGroup) -> None:
        """
        新たなグループを追加する
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




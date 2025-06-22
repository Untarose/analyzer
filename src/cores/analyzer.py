from abc import abstractmethod
from pathlib import Path
from interfaces.analyzer_interface import AnalyzerInterface
from cores.datagroup import DataGroup

class Analyzer(AnalyzerInterface):
    def __init__(self, groups: dict[str, DataGroup], root_directory: Path) -> None:
        self._groups = groups
        self._root_directory = root_directory

    @property
    def root_directory(self) -> Path:
        return self._root_directory

    def group_names(self) -> list[str]:
        return list(self._groups.keys())

    def delete_group(self, group_name: str) -> None:
        if not self.exist_group_name(group_name):
            raise ValueError(f"Group '{group_name}' does not exist.")
        del self._groups[group_name]
        # TODO: ディレクトリ/ファイルの削除処理も後日実装

    def get_group(self, group_name: str) -> DataGroup:
        if self.exist_group_name(group_name):
            return self._groups[group_name]
        else:
            raise ValueError(f"Group {group_name} does not exist")
        
    def _add_group(self, new_group: DataGroup) -> None:
        if self.exist_group_name(new_group.name):
            raise ValueError(f"DataGroup '{new_group.name}' already exists.")
        self._groups[new_group.name] = new_group
            

    def exist_group_name(self, group_name: str) -> bool:
        return group_name in self._groups

    def save_group(self, group_name: str) -> None:
        if not self.exist_group_name(group_name):
            raise ValueError(f"Group {group_name} does not exist")
        # TODO: 後日実装
        raise NotImplementedError("save_group() is not yet implemented.")

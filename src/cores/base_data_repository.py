from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from interfaces.data_repository import DataRepositoryInterface

class BaseDataRepository(DataRepositoryInterface):
    def __init__(self, root_directory: Path) -> None:
        self._root_directory = root_directory
    
    def _ensure_path_exists(self, path: Path) -> None:
        """
        pathに指定したディレクトリを作成する
        """
        path.parent.mkdir(parents=True, exist_ok=True)
    @abstractmethod
    def save(self, path: Path, df: pd.DataFrame) -> None:
        raise NotImplementedError
    @abstractmethod
    def load(self, path: Path) -> pd.DataFrame:
        raise NotImplementedError


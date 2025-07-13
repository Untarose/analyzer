from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
import pandas as pd
from interfaces.repository.data_repository_interface import DataRepositoryInterface

class BaseDataRepository(DataRepositoryInterface):
    def _ensure_path_exists(self, path: Path) -> None:
        """
        pathに指定したディレクトリを作成する
        """
        path.parent.mkdir(parents=True, exist_ok=True)
    @abstractmethod
    def save(self, path: Path, df: pd.DataFrame) -> None:
        raise NotImplementedError
    @abstractmethod
    def load(self, path: Path) -> object:
        raise NotImplementedError


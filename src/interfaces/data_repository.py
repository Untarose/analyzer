from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd

class DataRepositoryInterface(ABC):
    @abstractmethod
    def save(self, path:Path, df: pd.DataFrame) -> None:
        """
        データの保存処理
        """
        pass
    @abstractmethod
    def load(self, path: Path) -> pd.DataFrame:
        """
        データの読み込み処理
        """
        pass

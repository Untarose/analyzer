from pathlib import Path
from typing import List
import pandas as pd
from cores.base_data_repository import BaseDataRepository


class CSVDataRepository(BaseDataRepository):

    def save(self, path: Path, df: pd.DataFrame) -> None:
        """
        dfを保存する
        """
        self._ensure_path_exists(path)
        df.to_csv(path, index=False)

    def load(self, path: Path) -> pd.DataFrame:
        """
        dfを読み込む
        """
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            raise FileNotFoundError(f'file not found : {path}')
        except pd.errors.EmptyDataError:
            raise ValueError(f'csv file is empty: {path}')
        return df
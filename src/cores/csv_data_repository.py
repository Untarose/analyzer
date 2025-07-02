from pathlib import Path
from typing import List
import pandas as pd
from cores.base_data_repository import BaseDataRepository


class CSVDataRepository(BaseDataRepository):

    def save(self, path: Path, df: pd.DataFrame) -> None:
        """
        dfを保存する
        """
        csv_path = path.with_suffix('.csv')
        self._ensure_path_exists(csv_path)
        df.to_csv(csv_path, index=False)

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
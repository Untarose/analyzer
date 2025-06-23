from pathlib import Path
import pandas as pd
from cores.base_data_repository import BaseDataRepository


class CSVDataRepository(BaseDataRepository):
    def __init__(self, root_directory: Path) -> None:
        self._root_directory = root_directory

    def save(self, path: Path, df: pd.DataFrame) -> None:
        """
        dfを保存する
        """
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
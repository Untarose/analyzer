from pathlib import Path
from pandas import DataFrame
from typing import Tuple
from scipy.io import wavfile
import numpy as np
from cores.base_data_repository import BaseDataRepository

class WavDataRepository(BaseDataRepository):

    def save(self, path: Path, df: DataFrame) -> None:
        raise NotImplementedError
    
    def load(self, path: Path) -> Tuple[int, np.ndarray]:
        """
        WAVファイルを読み込む
        """
        rate, date = wavfile.read(path)
        return (rate, date)
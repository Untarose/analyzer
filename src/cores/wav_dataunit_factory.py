from pandas import DataFrame
from pathlib import Path
from typing import overload, Union, List
import numpy as np
from cores.base_dataunit_factory import BaseDataUnitFactory
from interfaces.dataunit_interface import DataUnitInterface
from cores.dataunit import DataUnit

class WavDataUnitFactory(BaseDataUnitFactory):
    def create(self, raw_data: tuple[int, np.ndarray], name: str, path: Path) -> list[DataUnitInterface]:
        rate, data = raw_data
        df_rate = DataFrame({'sample_rate': [rate]})
        if data.ndim == 1:
            df_waveform = DataFrame({
                'sample_index': np.arange(len(data)),
                'amplitude': data
            })
        elif data.ndim == 2 and data.shape[1] == 2:
            df_waveform = DataFrame({
                'sample_index': np.arange(len(data)),
                'left': data[:, 0],
                'right': data[:, 1]
            })
        else:
            raise ValueError(f"Unsupported WAV shape: {data.shape}")

        rate_name = f'{name}_rate'
        waveform_name = f'{name}_waveform'

        rate_path = path.with_stem(f'{path.stem}_rate')
        waveform_path = path.with_stem(f'{path.stem}_waveform')

        rate_meta = self._create_meta(name=rate_name, path=rate_path)
        waveform_meta = self._create_meta(name=waveform_name, path=waveform_path)
        
        return [DataUnit(df_rate, rate_meta), DataUnit(df_waveform, waveform_meta)]
    
    
    
    

    

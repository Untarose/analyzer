from pathlib import Path
import numpy as np

from cores.factory.wav_dataunit_factory import WavDataUnitFactory
from cores.data_unit.dataunit import DataUnit

def test_create_instance():
    factory = WavDataUnitFactory()

    raw_data = (40000, np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    name = 'wavsample'
    path = Path('/data/vault/wavsample')
    rate_name = f'{name}_rate'
    waveform_name = f'{name}_waveform'

    rate_path = path.with_stem(f'{path.stem}_rate')
    waveform_path = path.with_stem(f'{path.stem}_waveform')

    units = factory.create(raw_data=raw_data, name=name, path=path)

    assert units[0].name == rate_name
    assert units[1].name == waveform_name

    assert isinstance(units[0], DataUnit)
    assert isinstance(units[1], DataUnit)

    assert units[0].metadata.path == rate_path
    assert units[1].metadata.path == waveform_path

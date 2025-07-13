import numpy as np
from scipy.io import wavfile
from pathlib import Path
from cores.repository.wav_data_repository import WavDataRepository

def test_load_wav_file(tmp_path):
    # テスト用のwavファイルを作成
    sr = 16000  # サンプリングレート
    duration = 1.0  # 秒
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    wave = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

    wav_path = tmp_path / 'test.wav'
    wavfile.write(wav_path, sr, wave)

    # WavDataRepositoryで読み込む
    wav_data_repository = WavDataRepository()
    rate, data = wav_data_repository.load(wav_path)

    # assertion
    assert rate == sr
    assert isinstance(data, np.ndarray)
    assert data.shape == wave.shape
    assert np.allclose(data, wave, atol=1e-4)

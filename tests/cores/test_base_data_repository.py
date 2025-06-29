import shutil
from pathlib import Path
from cores.csv_data_repository import CSVDataRepository  # 例：継承しているクラス
import pandas as pd

def test_ensure_path_exists_creates_directory(tmp_path):
    # tmp_path は pytest の fixture（安全な一時パス）
    repo = CSVDataRepository()

    test_dir = tmp_path / "some" / "nested" / "dir"
    test_path = test_dir / "file.csv"

    # 念のため最初は存在していないことを確認
    assert not test_dir.exists()

    # _ensure_path_exists を使うため、save() を通じて使う or 明示的に呼ぶ
    repo._ensure_path_exists(test_path)

    # ディレクトリが作成されていることを確認
    assert test_dir.exists()
    assert test_dir.is_dir()

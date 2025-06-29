import pytest
import pandas as pd
from pathlib import Path

from cores.csv_data_repository import CSVDataRepository

def test_save_writes_correct_csv(tmp_path: Path):
    # 仮想保存ファイルpath
    file_path = tmp_path / 'new_file.csv'
    #CSVDataRepositryのインスタンス作成
    csv_data_repository = CSVDataRepository()
    # 保存するDataFrameを作成
    df = pd.DataFrame({'a': [1, 2]})
    # CSVDataRepository.saveで保存
    csv_data_repository.save(file_path, df=df)
    # 保存したDataFrameを読み込む
    load_csv = pd.read_csv(file_path)
    # ロードしたものが保存したものと同じかどうか
    assert load_csv.equals(df)

def test_load_read_correct_csv(tmp_path: Path):
    # 仮想保存ファイルpath
    file_path = tmp_path / 'old_file.csv'
    #CSVDataRepositryのインスタンス作成
    csv_data_repository = CSVDataRepository()
    # 保存するDataFrameを作成
    df = pd.DataFrame({'a': [1, 2]})
    # 読み込むためにDataFrameを保存する
    df.to_csv(file_path, index=False)
    # DataFrameを読み込む
    loaded_df = csv_data_repository.load(file_path)
    # 読み込んだDataFrameが同じかどうか
    assert loaded_df.equals(df)

def test_load_raise_file_not_found(tmp_path: Path):
    # 偽の保存パスを作成。ただし、ここに何も保存されていない。
    file_path = tmp_path / 'old_file.csv'
    # CSVDataRepositoryのインスタンス作成
    csv_data_repository = CSVDataRepository()
    # 偽の保存パスをロードしようとする
    with pytest.raises(FileNotFoundError):
        csv_data_repository.load(file_path)

def test_load_raise_empty_data_error(tmp_path: Path):
    # 偽の保存パスを作成。
    file_path = tmp_path / 'empty_file.csv'
    # 空のDataFrame
    empty_df = pd.DataFrame()
    #空のDataFrameを保存
    empty_df.to_csv(file_path, index=False)
    # CSVDataRepositoryのインスタンス作成
    csv_data_repository = CSVDataRepository()
    # 空のDataFrameをロードしようとする
    with pytest.raises(ValueError, match='csv file is empty'):
        csv_data_repository.load(file_path)
    
from datetime import datetime
from pathlib import Path
import pytest
import pandas as pd
from cores.dataunit import DataUnit
from cores.metas.dataunit_meta import DataUnitMeta
def test_create_dataunit_success():
    name = 'unit1'
    df = pd.DataFrame({'a': [1,2]})
    metadata = DataUnitMeta(
        name=name,
        path=Path('./aaa.csv'),
        created_at=datetime.now(),
        format='csv'
    )
    unit = DataUnit(df, metadata)
    assert unit.name == 'unit1'
    assert unit.df.equals(df)
    assert unit.metadata == metadata

def test_create_dataunit_empty_df_raises():
    name = 'unit1'
    df = pd.DataFrame()
    metadata = DataUnitMeta(
        name=name,
        path=Path('./aaa.csv'),
        created_at=datetime.now(),
        format='csv'
    )
    with pytest.raises(ValueError):
        DataUnit(df, metadata)

def test_with_updated_name():
    name = 'unit1'
    df = pd.DataFrame({'a': [1,2]})
    metadata = DataUnitMeta(
        name=name,
        path=Path('./aaa.csv'),
        created_at=datetime.now(),
        format='csv'
    )
    unit = DataUnit(df, metadata)
    new_name = 'new_unit'
    new_unit = unit.with_updated_name(new_name)
    assert new_unit.df.equals(df)
    assert new_unit.metadata.name == new_name
    assert unit.metadata.name == "unit1"  # イミュータブル確認

def test_with_updated_df():
    df1 = pd.DataFrame({'a': [1]})
    df2 = pd.DataFrame({'b': [2]})
    name = 'unit1'
    metadata = DataUnitMeta(
        name=name,
        path=Path('./aaa.csv'),
        created_at=datetime.now(),
        format='csv'
    )
    unit = DataUnit(df1, metadata)
    new_unit = unit.with_updated_df(df2)
    assert new_unit.df.equals(df2)
    assert unit.df.equals(df1) # イミュータブル確認

def test_with_updated_metadata():
    df = pd.DataFrame({'a': [1]})
    
    name_1 = 'unit1'
    metadata_1 = DataUnitMeta(
        name=name_1,
        path=Path('./aaa.csv'),
        created_at=datetime.now(),
        format='csv'
    )
    unit = DataUnit(df, metadata_1)

    new_unit = unit.with_update_metadata("format", "json")
    assert new_unit.metadata.format == "json"

    assert unit.metadata == metadata_1  # イミュータブル確認

    with pytest.raises(AttributeError):
        new_unit = unit.with_update_metadata("unknown_key", 'hello')
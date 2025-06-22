import pytest
import pandas as pd
from cores.dataunit import DataUnit

def test_create_dataunit_success():
    name = 'unit1'
    df = pd.DataFrame({'a': [1,2]})
    metadata = {'source': 'test'}
    unit = DataUnit(name, df, metadata)
    assert unit.name == 'unit1'
    assert unit.df.equals(df)
    assert unit.metadata == metadata

def test_create_dataunit_empty_name_raises():
    df = pd.DataFrame({'a': [1]})
    with pytest.raises(ValueError):
        DataUnit('', df, {})

def test_create_dataunit_empty_df_raises():
    df = pd.DataFrame()
    with pytest.raises(ValueError):
        DataUnit('a', df, {})

def test_with_updated_name():
    df = pd.DataFrame({'a': [1]})
    unit = DataUnit("unit", df, {})
    new_unit = unit.with_updated_name("new_unit")
    assert new_unit.name == "new_unit"
    assert new_unit.df.equals(df)
    assert new_unit.metadata == unit.metadata
    assert unit.name == "unit"  # イミュータブル確認

def test_with_updated_df():
    df1 = pd.DataFrame({'a': [1]})
    df2 = pd.DataFrame({'b': [2]})
    unit = DataUnit('unit', df1, {})
    new_unit = unit.with_updated_df(df2)
    assert new_unit.df.equals(df2)
    assert unit.df.equals(df1) # イミュータブル確認

def test_with_update_metadata():
    df = pd.DataFrame({'a': [1]})
    unit = DataUnit("unit", df, {"source": "raw"})
    new_unit = unit.with_update_metadata("stage", "cleaned")
    assert new_unit.metadata == {"source": "raw", "stage": "cleaned"}
    assert unit.metadata == {"source": "raw"}  # イミュータブル確認
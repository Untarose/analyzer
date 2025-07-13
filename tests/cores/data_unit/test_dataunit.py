from datetime import datetime
from pathlib import Path
import pytest
import pandas as pd
from cores.data_unit.dataunit import DataUnit
from cores.metas.dataunit_meta import DataUnitMeta
def test_create_dataunit_success():
    name = 'unit1'
    df = pd.DataFrame({'a': [1,2]})
    metadata = DataUnitMeta(
        name=name,
        path=Path('./aaa.csv'),
        created_at=datetime.now()
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
        created_at=datetime.now()
    )
    with pytest.raises(ValueError):
        DataUnit(df, metadata)

def test_with_updated_name():
    name = 'unit1'
    df = pd.DataFrame({'a': [1,2]})
    metadata = DataUnitMeta(
        name=name,
        path=Path('./aaa.csv'),
        created_at=datetime.now()
    )
    unit = DataUnit(df, metadata)
    new_name = 'new_unit'
    new_unit = unit.with_updated_name(new_name)
    assert new_unit.df.equals(df)
    assert new_unit.metadata.name == new_name
    assert unit.metadata.name == "unit1"  # イミュータブル確認
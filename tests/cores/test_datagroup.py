import pytest
import pandas as pd
from pathlib import Path
from cores.datagroup import DataGroup
from cores.dataunit import DataUnit
from cores.metas.datagroup_meta import DataGroupMeta
from cores.metas.dataunit_meta import DataUnitMeta
def test_create_datagroup_success(tmp_path):
    # unit 1
    df_unit_1 = pd.DataFrame({'a': [1, 2]})
    metadata_unit_1 = DataUnitMeta(
        name = 'unit_1',
        path = Path('./group_1/unit_1.csv')
    )
    unit_1 = DataUnit(df_unit_1, metadata_unit_1)

    # unit 2
    df_unit_2 = pd.DataFrame({'b': [3, 4]})
    metadata_unit_2 = DataUnitMeta(
        name = 'unit_2',
        path = Path('./group_1/unit_2.csv')
    )
    unit_2 = DataUnit(df_unit_2, metadata_unit_2)

    # units
    units = {unit_1.name: unit_1, unit_2.name: unit_2}

    # make DataGroup
    group_name = 'group_1'
    group_path = Path('./group_1')
    metadata_group_1 = DataGroupMeta(
        name = group_name,
        path = group_path,
    )
    group = DataGroup(units, metadata_group_1)

    #check
    for name in units:
        assert group.get_unit(name) is units[name], f'{name} is not the same object'
    
    assert set(group.units.keys()) == set(units.keys())

    assert set(units.keys()) == set(group.unit_names())

    assert group.name == group_name

    assert group.path == group_path

def test_get_unit_unknown_name_raises(tmp_path):
    # unit 1
    df_unit_1 = pd.DataFrame({'a': [1, 2]})
    metadata_unit_1 = DataUnitMeta(
        name = 'unit_1',
        path = Path('./group_1/unit_1.csv')
    )
    unit_1 = DataUnit(df_unit_1, metadata_unit_1)

    # unit 2
    df_unit_2 = pd.DataFrame({'b': [3, 4]})
    metadata_unit_2 = DataUnitMeta(
        name = 'unit_2',
        path = Path('./group_1/unit_2.csv')
    )
    unit_2 = DataUnit(df_unit_2, metadata_unit_2)

    # units
    units = {unit_1.name: unit_1, unit_2.name: unit_2}

    # make DataGroup
    group_name = 'group_1'
    group_path = Path('./group_1')
    metadata_group_1 = DataGroupMeta(
        name = group_name,
        path = group_path,
    )
    group = DataGroup(units, metadata_group_1)

    with pytest.raises(ValueError):
        group.get_unit('unit_3')
        group.get_unit('')

def test_with_updated_name():
    # unit 1
    df_unit_1 = pd.DataFrame({'a': [1, 2]})
    metadata_unit_1 = DataUnitMeta(
        name = 'unit_1',
        path = Path('./group_1/unit_1.csv')
    )
    unit_1 = DataUnit(df_unit_1, metadata_unit_1)

    # unit 2
    df_unit_2 = pd.DataFrame({'b': [3, 4]})
    metadata_unit_2 = DataUnitMeta(
        name = 'unit_2',
        path = Path('./group_1/unit_2.csv')
    )
    unit_2 = DataUnit(df_unit_2, metadata_unit_2)

    # units
    units = {unit_1.name: unit_1, unit_2.name: unit_2}

    # make DataGroup
    group_name = 'group_1'
    group_path = Path('./group_1')
    metadata_group_1 = DataGroupMeta(
        name = group_name,
        path = group_path,
    )
    group = DataGroup(units, metadata_group_1)
    # new group name
    new_name = 'new_group'
    # new group instance
    new_group = group.with_update_name(new_name)
    # check
    assert new_group.name == new_name

def test_with_updated_meta():
    # unit 1
    df_unit_1 = pd.DataFrame({'a': [1, 2]})
    metadata_unit_1 = DataUnitMeta(
        name = 'unit_1',
        path = Path('./group_1/unit_1.csv')
    )
    unit_1 = DataUnit(df_unit_1, metadata_unit_1)

    # unit 2
    df_unit_2 = pd.DataFrame({'b': [3, 4]})
    metadata_unit_2 = DataUnitMeta(
        name = 'unit_2',
        path = Path('./group_1/unit_2.csv')
    )
    unit_2 = DataUnit(df_unit_2, metadata_unit_2)

    # units
    units = {unit_1.name: unit_1, unit_2.name: unit_2}

    # make DataGroup
    group_name = 'group_1'
    group_path = Path('./group_1')
    metadata_group_1 = DataGroupMeta(
        name = group_name,
        path = group_path,
    )
    group = DataGroup(units, metadata_group_1)
    # new meta field
        
    

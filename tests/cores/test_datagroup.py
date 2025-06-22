import pytest
import pandas as pd
from pathlib import Path
from cores.datagroup import DataGroup
from cores.dataunit import DataUnit

def test_create_datagroup_success(tmp_path):
    # unit 1
    name_unit_1 = 'unit_1'
    df_unit_1 = pd.DataFrame({'a': [1, 2]})
    metadata_unit_1 = {'source': 'test'}
    unit_1 = DataUnit(name_unit_1, df_unit_1, metadata_unit_1)

    # unit 2
    name_unit_2 = 'unit_2'
    df_unit_2 = pd.DataFrame({'b': [3, 4]})
    metadata_unit_2 = {'date': '2025-06-22'}
    unit_2 = DataUnit(name_unit_2, df_unit_2, metadata_unit_2)

    # units
    units = {unit_1.name: unit_1, unit_2.name: unit_2}

    # make DataGroup
    group_name = 'group_1'
    group_path = tmp_path / 'aaabbbccc'
    group = DataGroup(group_name ,units, group_path)

    #check
    for name in units:
        assert group.get_unit(name) is units[name], f'{name} is not the same object'
    
    assert set(group.units.keys()) == set(units.keys())

    assert set(units.keys()) == set(group.unit_names())

    assert group.name == group_name

    assert group.path == group_path

def test_get_unit_unknown_name_raises(tmp_path):
    # unit 1
    name_unit_1 = 'unit_1'
    df_unit_1 = pd.DataFrame({'a': [1, 2]})
    metadata_unit_1 = {'source': 'test'}
    unit_1 = DataUnit(name_unit_1, df_unit_1, metadata_unit_1)

    # unit 2
    name_unit_2 = 'unit_2'
    df_unit_2 = pd.DataFrame({'b': [3, 4]})
    metadata_unit_2 = {'date': '2025-06-22'}
    unit_2 = DataUnit(name_unit_2, df_unit_2, metadata_unit_2)

    # units
    units = {unit_1.name: unit_1, unit_2.name: unit_2}

    # make DataGroup
    group_name = 'group_1'
    group_path = tmp_path / 'aaabbbccc'
    group = DataGroup(group_name ,units, group_path)

    with pytest.raises(ValueError):
        group.get_unit('unit_3')
        group.get_unit('')
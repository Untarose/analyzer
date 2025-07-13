from pandas import DataFrame
from pathlib import Path
import pytest
from cores.data_unit.dataunit import DataUnit
from cores.data_group.datagroup import DataGroup
from cores.builder.data_builder import DataBuilder
from cores.factory.default_dataunit_factory import DefaultDataUnitFactory
from cores.factory.default_datagroup_factory import DefaultDataGroupFactory
from cores.metas.datagroup_meta import DataGroupMeta
from cores.metas.dataunit_meta import DataUnitMeta

def test_group_to_dict(tmp_path):
    group_master_path = Path(tmp_path)
    
    group_name1 = 'group1'
    group_path1 = group_master_path / group_name1
    
    dataunit_factory= DefaultDataUnitFactory()
    datagroup_factory = DefaultDataGroupFactory()
    df1 = DataFrame([1,1,1,1,1,1])
    unit_name1 = 'a'
    unit_path1 = group_path1 / unit_name1
    unit1 = dataunit_factory.create(
        df1, unit_name1, unit_path1
    )
    df2 = DataFrame([2,2,2,2,2,2])
    unit_name2 = 'b'
    unit_path2 = group_path1 / unit_name2
    unit2 = dataunit_factory.create(
        df2, unit_name2, unit_path2
    )
    
    group1 = datagroup_factory.create(
        [unit1[0], unit2[0]],
        group_name1,
        group_path1
    )
    
    group_name2 = 'group2'
    group_path2 = group_master_path / group_name2
    
    df3 = DataFrame([1,1,1,1,1,1])
    unit_name3 = 'c'
    unit_path3 = group_path2 / unit_name3
    unit3 = dataunit_factory.create(
        df3, unit_name3, unit_path3
    )
    df4 = DataFrame([2,2,2,2,2,2])
    unit_name4 = 'd'
    unit_path4 = group_path2 / unit_name4
    unit4 = dataunit_factory.create(
        df4, unit_name4, unit_path4
    )
    
    group2 = datagroup_factory.create(
        [unit3[0], unit4[0]],
        group_name2,
        group_path2
    )
    
    data_builder = DataBuilder(dataunit_factory=dataunit_factory, datagroup_factory=datagroup_factory)
    
    data = data_builder.group_to_dict(
        groups = [group1, group2],
        units_selection = {'group1': ['a'], 'group2': ['c']}
    )
    assert group_name1 in data.keys()
    assert unit_name1 in data['group1'].keys()
    assert unit_name2 not in data['group1'].keys()
    assert data['group1']['a'].equals(df1)
    
    assert group_name2 in data.keys()
    assert unit_name3 in data['group2'].keys()
    assert unit_name4 not in data['group2'].keys()
    assert data['group2']['c'].equals(df3)
    
def test_group_to_dict_all_unit_in_group(tmp_path):
    group_master_path = Path(tmp_path)
    
    group_name1 = 'group1'
    group_path1 = group_master_path / group_name1
    
    dataunit_factory= DefaultDataUnitFactory()
    datagroup_factory = DefaultDataGroupFactory()
    df1 = DataFrame([1,1,1,1,1,1])
    unit_name1 = 'a'
    unit_path1 = group_path1 / unit_name1
    unit1 = dataunit_factory.create(
        df1, unit_name1, unit_path1
    )
    df2 = DataFrame([2,2,2,2,2,2])
    unit_name2 = 'b'
    unit_path2 = group_path1 / unit_name2
    unit2 = dataunit_factory.create(
        df2, unit_name2, unit_path2
    )
    
    group1 = datagroup_factory.create(
        [unit1[0], unit2[0]],
        group_name1,
        group_path1
    )
    
    data_builder = DataBuilder(dataunit_factory=dataunit_factory, datagroup_factory=datagroup_factory)
    
    data = data_builder.group_to_dict(
        groups = [group1],
        units_selection = {'group1': []}
    )
    
    assert set(list(data['group1'].keys())) == set([unit_name1, unit_name2])
    assert data['group1']['a'].equals(df1)
    assert data['group1']['b'].equals(df2)
    
def test_dict_to_group(tmp_path):
    df1 = DataFrame([1,1,1,1,1,1,1])
    df2 = DataFrame([2,2,2,2,2,2,2])
    df3 = DataFrame([3,3,3,3,3,3,3])
    
    group_name1 = 'group1'
    group_name2 = 'group2'
    
    unit_name1 = 'a'
    unit_name2 = 'b'
    unit_name3 = 'c'
    
    data = {
        group_name1: {
            unit_name1: df1, unit_name2: df2
        },
        group_name2: {
            unit_name3: df3, unit_name1: df1
        }
    }
    dataunit_factory= DefaultDataUnitFactory()
    datagroup_factory = DefaultDataGroupFactory()
    data_builder = DataBuilder(dataunit_factory=dataunit_factory, datagroup_factory=datagroup_factory)
    
    groups = data_builder.dict_to_group(
        groups_dict=data,
        parent_path=tmp_path
    )
    assert groups[0].name == group_name1
    assert groups[1].name == group_name2
    
    assert set(groups[0].unit_names()) == set([unit_name1, unit_name2])
    assert set(groups[1].unit_names()) == set([unit_name3, unit_name1])
    assert groups[0].get_unit(unit_name=unit_name1).df.equals(df1)
    assert groups[0].get_unit(unit_name=unit_name2).df.equals(df2)
    assert groups[1].get_unit(unit_name=unit_name3).df.equals(df3)
    assert groups[1].get_unit(unit_name=unit_name1).df.equals(df1)
    
    
        
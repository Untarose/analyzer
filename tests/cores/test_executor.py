from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Callable
from pandas import DataFrame
import os
import pytest

from cores.exec_context import ExecContext
from interfaces.ExecutorInterface import ExecutorInterface
from interfaces.data_builder_interface import DataBuilderInterface
from interfaces.datagroup_interface import DataGroupInterface
from interfaces.dataunit_interface import DataUnitInterface
from cores.default_datagroup_factory import DefaultDataGroupFactory
from cores.default_dataunit_factory import DefaultDataUnitFactory
from cores.data_builder import DataBuilder
from cores.executor import Executor
from cores.metas.dataunit_meta import DataUnitMeta
from cores.metas.datagroup_meta import DataGroupMeta
from cores.dataunit import DataUnit
from cores.datagroup import DataGroup
from cores.analyzer import Analyzer
@pytest.fixture
def sample_analyzer(tmp_path):
    # vault と master を先に作っておく
    (tmp_path / "vault").mkdir()
    master_path = tmp_path / 'master'
    master_path.mkdir()
    path_1 = master_path / 'group1tmp'
    path_2 = master_path / 'group2tmp'
    (path_1).mkdir()
    (path_2).mkdir()
    
    # ユニット1の作成
    unit_meta_1 = DataUnitMeta(name="unit1", path=path_1 / "unit1")
    unit_1 = DataUnit(df=DataFrame({"a": [1, 2]}), metadata=unit_meta_1)

    # グループ1の作成
    group_meta_1 = DataGroupMeta(name="group1", path=path_1)
    group_1 = DataGroup(units={unit_1.name: unit_1}, meta=group_meta_1)

    # ユニット2の作成
    unit_meta_2 = DataUnitMeta(name="unit2", path=path_2 / "unit2")
    unit_2 = DataUnit(df=DataFrame({"b": [1, 2]}), metadata=unit_meta_2)

    # グループ2の作成
    group__meta_2 = DataGroupMeta(name="group2", path=path_2)
    group_2 = DataGroup(units={unit_2.name: unit_2}, meta=group__meta_2)

    # Analyzer の作成と登録
    analyzer = Analyzer(str(tmp_path))
    analyzer._add_group(group_1)
    analyzer._add_group(group_2)
    return analyzer
def test_exec(sample_analyzer):
    analyzer = sample_analyzer
    
    unit_factory = DefaultDataUnitFactory()
    group_factory = DefaultDataGroupFactory()
    builder = DataBuilder(unit_factory, group_factory)
    executor = Executor(builder)
    
    group1 = analyzer.get_group('group1')
    group2 = analyzer.get_group('group2')
    groups = [group1, group2]
    
    def times_x_and_add_y_other_groups(group1: dict[str, DataFrame], group2: dict[str, DataFrame], x, y):
        df1 = group1['unit1']
        df2 = group2['unit2']
        new_df1_1 = df1.copy()
        new_df1_2 = df1.copy()
        new_df2_1 = df2.copy()
        new_df2_2 = df2.copy()
        new_df1_1['a'] = df1['a'].apply(lambda i: i * x)
        new_df1_2['a'] = df1['a'].apply(lambda i: i + y)
        new_df2_1['b'] = df2['b'].apply(lambda i: i * x) 
        new_df2_2['b'] = df2['b'].apply(lambda i: i + y)
        
        result_groups_dict = {
            'newgroup1': {'a': new_df1_1},
            'newgroup2': {'b': new_df1_2},
            'newgroup3': {'c': new_df2_1},
            'newgroup4': {'d': new_df2_2}
        }
        return result_groups_dict
    exec_context = ExecContext(
        func=times_x_and_add_y_other_groups,
        units_selection={
            'group1': [],
            'group2': []
        },
        kwargs={'x': 3, 'y': 10000}
    )
    
    new_groups = executor.exec(executor_context=exec_context, groups=groups)
    
    expect_new_group_names = [f'newgroup{i}' for i in range(1, 5, 1)]
    
    assert set(expect_new_group_names) == set([group.name for group in new_groups])
    
    df1 = analyzer.get_group('group1').get_unit('unit1').df
    df2 = analyzer.get_group('group2').get_unit('unit2').df
    new_df1_1 = df1.apply(lambda x: x*3)
    new_df1_2 = df1.apply(lambda y: y + 10000)
    new_df2_1 = df2.apply(lambda x: x*3)
    new_df2_2 = df2.apply(lambda y: y + 10000)
    group_map = {group.name: group for group in new_groups}
    for expected in expect_new_group_names:
        assert expected in group_map, f"Expected group '{expected}' not found in result"
    assert group_map['newgroup1'].get_unit('a').df.equals(new_df1_1)
    assert group_map['newgroup2'].get_unit('b').df.equals(new_df1_2)
    assert group_map['newgroup3'].get_unit('c').df.equals(new_df2_1)
    assert group_map['newgroup4'].get_unit('d').df.equals(new_df2_2)
    
def test_is_expext_result():
    # Executorを構築（BuilderだけでOK）
    builder = DataBuilder(DefaultDataUnitFactory(), DefaultDataGroupFactory())
    executor = Executor(builder)

    # --- 1: 正常な返り値
    valid_result = {
        "group1": {
            "unit1": DataFrame({"a": [1, 2]})
        }
    }
    assert executor._is_expext_result(valid_result) is True

    # --- 2: トップがdictじゃない
    not_dict = ["not", "a", "dict"]
    assert executor._is_expext_result(not_dict) is False

    # --- 3: unit_dictがdictじゃない
    bad_unit_dict = {
        "group1": [DataFrame({"a": [1, 2]})]
    }
    assert executor._is_expext_result(bad_unit_dict) is False

    # --- 4: unitの中身がDataFrameじゃない
    not_df = {
        "group1": {
            "unit1": [1, 2, 3]
        }
    }
    assert executor._is_expext_result(not_df) is False


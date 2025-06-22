import pytest
import pandas as pd
from pathlib import Path
from cores.analyzer import Analyzer
from cores.dataunit import DataUnit
from cores.datagroup import DataGroup

@pytest.fixture
def sample_analyzer(tmp_path):
    unit_1 = DataUnit("unit1", df=pd.DataFrame({"a": [1, 2]}), metadata={})
    unit_2 = DataUnit("unit2", df=pd.DataFrame({"b": [3, 4]}), metadata={})
    group = DataGroup(name="group1", units={unit_1.name: unit_1, unit_2.name: unit_2}, path=tmp_path / "group1")
    return Analyzer(groups={group.name: group}, root_directory=tmp_path)

def test_group_names(sample_analyzer):
    assert "group1" in sample_analyzer.group_names()

def test_get_group_success(sample_analyzer):
    group = sample_analyzer.get_group("group1")
    assert group.name == "group1"

def test_get_group_not_exist(sample_analyzer):
    with pytest.raises(ValueError):
        sample_analyzer.get_group("not_exist")

def test_add_group_already_exists(sample_analyzer):
    group = sample_analyzer.get_group("group1")
    with pytest.raises(ValueError):
        sample_analyzer._add_group(group)

def test_exist_group_name(sample_analyzer):
    assert sample_analyzer.exist_group_name("group1")
    assert not sample_analyzer.exist_group_name("unknown")

def test_delete_group(sample_analyzer):
    sample_analyzer.delete_group("group1")
    assert not sample_analyzer.exist_group_name("group1")

def test_save_group_not_implemented(sample_analyzer):
    with pytest.raises(NotImplementedError):
        sample_analyzer.save_group("group1")

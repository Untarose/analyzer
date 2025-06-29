from pathlib import Path
from pandas import DataFrame
import pytest

from interfaces.datagroup_interface import DataGroupInterface
from interfaces.dataunit_interface  import DataUnitInterface
from interfaces.datagroup_factory_interface import DataGroupFactoryInterface
from cores.metas.datagroup_meta import DataGroupMeta
from cores.datagroup import DataGroup
from cores.dataunit import DataUnit
from cores.default_dataunit_factory import DefaultDataUnitFactory
from cores.default_datagroup_factory import DefaultDataGroupFactory
def test_create_instance():
    dataunit_factory = DefaultDataUnitFactory()
    path = Path('./aaa/bbb/ccc.csv')
    unit_name = 'unit1'
    unit = dataunit_factory.create(DataFrame({'a':[1, 2]}),unit_name,path)

    group_name = 'gtoup_1'
    group_path = './aaa/ccc'
    datagroup_factory = DefaultDataGroupFactory()
    group = datagroup_factory.create(unit, group_name, group_path)

    # assertion
    assert group.name == group_name
    assert group.path == group_path
    assert group.exist_unit_name(unit_name)
    assert group.get_unit(unit_name) == unit[0]

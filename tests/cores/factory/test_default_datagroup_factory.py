from pathlib import Path
from pandas import DataFrame
import pytest

from interfaces.data_group.datagroup_interface import DataGroupInterface
from interfaces.data_unit.dataunit_interface  import DataUnitInterface
from interfaces.factory.datagroup_factory_interface import DataGroupFactoryInterface
from cores.metas.datagroup_meta import DataGroupMeta
from cores.data_group.datagroup import DataGroup
from cores.data_unit.dataunit import DataUnit
from cores.factory.default_dataunit_factory import DefaultDataUnitFactory
from cores.factory.default_datagroup_factory import DefaultDataGroupFactory
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

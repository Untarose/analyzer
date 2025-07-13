from pandas import DataFrame
from pathlib import Path

from cores.factory.default_dataunit_factory import DefaultDataUnitFactory

def test_create_instance():
    factory = DefaultDataUnitFactory()
    df = DataFrame({'a': [1, 2]})
    name = 'unit1'
    path = Path('./group')/name

    dataunit = factory.create(df, name, path)

    assert dataunit[0].name == name
    assert dataunit[0].df.equals(df)
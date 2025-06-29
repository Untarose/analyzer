from pathlib import Path
from pandas.core.api import DataFrame
from cores.base_dataunit_factory import BaseDataUnitFactory
from cores.dataunit import DataUnit
from interfaces.dataunit_interface import DataUnitInterface

class DummyDataUnitFactory(BaseDataUnitFactory):
    def create(self, raw_data: object, name: str, path: Path) -> list[DataUnitInterface]:
        df = DataFrame({'a': [1, 2]})
        return [DataUnit(df=df, metadata=self._create_meta(name, path))]



def test_create_meta():
    name = 'unit_1'
    path = Path('./group/unit_1')
    dummyDataUnitFactory = DummyDataUnitFactory()
    dataunit = dummyDataUnitFactory._create_meta(
        name=name,
        path=path
    )
    assert dataunit.name == name

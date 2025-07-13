from pathlib import Path
from pandas import DataFrame

from cores.factory.base_dataunit_factory import BaseDataUnitFactory
from interfaces.data_unit.dataunit_interface import DataUnitInterface
from cores.data_unit.dataunit import DataUnit

class DefaultDataUnitFactory(BaseDataUnitFactory):
    def create(self, raw_data: DataFrame, name: str, path: Path) -> list[DataUnitInterface]:
        metadata = self._create_meta(name=name, path=path)
        return [DataUnit(df=raw_data, metadata=metadata)]
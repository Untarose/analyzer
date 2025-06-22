from pathlib import Path
from interfaces.datagroup_interface  import DataGroupInterface
from cores.dataunit import DataUnit

class DataGroup(DataGroupInterface):

    def __init__(self, name ,units: dict[str, DataUnit], path: Path) -> None:
        self._name = name
        self._units = units
        self._path = path.resolve()

    @property
    def name(self) -> str:
        return self._name

    @property
    def units(self) -> dict[str, DataUnit]:
        """
        辞書型のDataUnitの一覧を返す
        """
        return self._units
    
    @property
    def path(self) -> Path:
        return self._path

    def get_unit(self, unit_name: str) -> DataUnit:
        """
        指定したnameをもつDataUnitを返す
        """
        if self.exist_unit_name(unit_name):
            return self.units[unit_name]
        else:
            raise ValueError(f'your specified {unit_name} is not exist')

    def exist_unit_name(self, unit_name: str) -> bool:
        """
        指定したnameをもつunitを持っているか
        """
        return unit_name in self.unit_names()

    def unit_names(self) -> list[str]:
        """
        unitsの名前列を返す
        """
        return list(self._units.keys())

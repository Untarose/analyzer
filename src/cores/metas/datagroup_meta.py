from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Optional
from interfaces.meta_interface import MetaInterface

@dataclass
class DataGroupMeta(MetaInterface):
    name: str
    path: Path
    created_at: Optional[datetime] = field(default_factory=lambda:datetime.now()) # 初期値を現在の時間にする

    def __post_init__(self):
        if not self.name:
            raise ValueError(f'{self.__class__.__name__}: name must not be empty.')
        if self._is_invalid_path():
            raise ValueError(f'{self.__class__.__name__}: path must not be empty.')
        
    def _is_invalid_path(self) -> bool:
        return not str(self.path).strip() or str(self.path) in {".", "./"}
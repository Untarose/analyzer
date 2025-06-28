from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import Optional
from interfaces.meta_interface import MetaInterface

@dataclass
class DataUnitMeta(MetaInterface):
    name: str
    path: Path
    created_at: Optional[datetime] = None
    format: Optional[str] = None

    def __post_init__(self):
        if not self.name:
            raise ValueError('name must not be empty.')
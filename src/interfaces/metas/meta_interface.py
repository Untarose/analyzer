from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import Optional, Protocol

class MetaInterface(Protocol):
    name: str
    path: Path
    created_at: datetime

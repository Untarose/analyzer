import pytest
from pathlib import Path
from datetime import datetime
from cores.metas.datagroup_meta import DataGroupMeta

def test_init_datagroup_meta_success():
    name = 'datagroup'
    path = Path('./tmp')
    created_at = datetime.now()

    unit_meta = DataGroupMeta(
        name,
        path,
        created_at
    )

    assert unit_meta.name == name
    assert unit_meta.path == path
    assert unit_meta.created_at == created_at

def test_init_datagroup_name_value_error():
    name = ''
    path = Path('./tmp')
    created_at = datetime.now()
    with pytest.raises(ValueError):
        unit_meta = DataGroupMeta(
            name,
            path,
            created_at
        )

def test_init_datagroup_path_value_error():
    name = 'datagroup'
    path = Path('')
    created_at = datetime.now()
    with pytest.raises(ValueError):
        unit_meta = DataGroupMeta(
            name,
            path,
            created_at
        )
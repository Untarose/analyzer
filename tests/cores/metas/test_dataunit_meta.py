import pytest
from pathlib import Path
from datetime import datetime
from cores.metas.dataunit_meta import DataUnitMeta

def test_init_dataunit_meta_success():
    name = 'dataunit'
    path = Path('./tmp/a.csv')
    created_at = datetime.now()
    format = 'csv'

    unit_meta = DataUnitMeta(
        name,
        path,
        created_at,
        format
    )

    assert unit_meta.name == name
    assert unit_meta.path == path
    assert unit_meta.created_at == created_at
    assert unit_meta.format == format

def test_init_dataunit_name_value_error():
    name = ''
    path = Path('./tmp/a.csv')
    created_at = datetime.now()
    format = 'csv'
    with pytest.raises(ValueError):
        unit_meta = DataUnitMeta(
            name,
            path,
            created_at,
            format
        )
def test_init_dataunit_path_value_error():
    name = 'unit'
    path = Path('')
    created_at = datetime.now()
    format = 'csv'
    with pytest.raises(ValueError):
        unit_meta = DataUnitMeta(
            name,
            path,
            created_at,
            format
        )

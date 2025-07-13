from pandas import DataFrame
import pytest
from cores.executor.exec_context import ExecContext

def test_init_exec_context():
    def test(box1: dict[str, dict[str, DataFrame]], box2: dict[str, dict[str, DataFrame]]):
        pass
    units_selection = {
        'box1': [
            'table1',
            'table2',
            'table3'
        ],
        'box2': []
    }
    ec = ExecContext(func=test, units_selection=units_selection)
    assert ec.func == test
    assert ec.units_selection == units_selection

def test_validation_func_arg_error_value_error():
    def test1(box1: dict[str, dict[str, DataFrame]], box2: dict[str, dict[str, DataFrame]]):
        pass
    units_selection1= {
        'box3': [
            'table1',
            'table2',
            'table3'
        ]
    }
    with pytest.raises(ValueError) as e:
        ec = ExecContext(func=test1, units_selection=units_selection1)
    assert 'box1' in str(e.value)
    assert 'box2' in str(e.value)
    assert 'box3' in str(e.value)
    
    def test2(box1: dict[str, dict[str, DataFrame]], box2: dict[str, dict[str, DataFrame]]):
        pass
    units_selection2 = {
        'box1': [
            'table1',
            'table2',
            'table3'
        ],
        'box2': [],
        'box3': [
            'table11'
        ]
    }
    with pytest.raises(ValueError) as e:
        ec = ExecContext(func=test2, units_selection=units_selection2)
    assert 'box1' not in str(e.value)
    assert 'box2' not in str(e.value)
    assert 'box3' in str(e.value)
    
    def test3(box1: dict[str, dict[str, DataFrame]], box2: dict[str, dict[str, DataFrame]], **kwargs):
        pass
    units_selection3= {
        'box1': [
            'table1',
            'table2',
            'table3'
        ],
        'box2':[

        ]
    }

    kwargs3 = {'test_num': 1}

    with pytest.raises(ValueError) as e:
        ec = ExecContext(func=test3, units_selection=units_selection3, kwargs=kwargs3)
    assert 'box1' not in str(e.value)
    assert 'box2' not in str(e.value)
    assert '**kwargs' in str(e.value)

    def test4(box1: dict[str, dict[str, DataFrame]], box2: dict[str, dict[str, DataFrame]]):
        pass
    units_selection4= {
        'box1': [
            'table1',
            'table2',
            'table3'
        ],
        'box2':[

        ]
    }

    kwargs4 = {'test_num': 1}

    with pytest.raises(ValueError) as e:
        ec = ExecContext(func=test4, units_selection=units_selection4, kwargs=kwargs4)
    assert 'box1' not in str(e.value)
    assert 'box2' not in str(e.value)
    assert 'test_num' in str(e.value)

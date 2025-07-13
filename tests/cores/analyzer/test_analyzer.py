import pytest
import pandas as pd
from pathlib import Path
from cores.analyzer.analyzer import Analyzer
from cores.data_unit.dataunit import DataUnit
from cores.data_group.datagroup import DataGroup
from cores.metas.datagroup_meta import DataGroupMeta
from cores.metas.dataunit_meta import DataUnitMeta

from cores.factory.default_dataunit_factory import DefaultDataUnitFactory
from cores.factory.default_datagroup_factory import DefaultDataGroupFactory
from cores.builder.data_builder import DataBuilder
from cores.executor.executor import Executor
from cores.executor.exec_context import ExecContext


@pytest.fixture
def sample_analyzer(tmp_path):
    # vault と master を先に作っておく
    (tmp_path / "vault").mkdir()
    (tmp_path / "master").mkdir()

    # ユニットの作成
    unit_meta = DataUnitMeta(name="unit1", path=tmp_path / "unit1.csv")
    unit = DataUnit(df=pd.DataFrame({"a": [1, 2]}), metadata=unit_meta)

    # グループの作成
    group_meta = DataGroupMeta(name="group1", path=tmp_path / "group1")
    group = DataGroup(units={unit.name: unit}, meta=group_meta)

    # Analyzer の作成と登録
    analyzer = Analyzer(str(tmp_path))
    analyzer._add_group(group)
    return analyzer


def test_group_names(sample_analyzer):
    assert "group1" in sample_analyzer.group_names()

def test_get_group_success(sample_analyzer):
    group = sample_analyzer.get_group("group1")
    assert group.name == "group1"

def test_get_group_not_exist(sample_analyzer):
    with pytest.raises(ValueError):
        sample_analyzer.get_group("not_exist")

def test_add_group_already_exists(sample_analyzer):
    group = sample_analyzer.get_group("group1")
    with pytest.raises(ValueError):
        sample_analyzer._add_group(group)

def test_exist_group_name(sample_analyzer):
    assert sample_analyzer.exist_group_name("group1")
    assert not sample_analyzer.exist_group_name("unknown")

def test_delete_group(sample_analyzer):
    sample_analyzer.delete_group("group1")
    assert not sample_analyzer.exist_group_name("group1")

def test_load_groups_from_vault(tmp_path: Path):
    # 正しい Vault 構造（vault/group1/__DATA__/data.csv）
    group_dir = tmp_path / "vault" / "group1"
    data_dir = group_dir / "__DATA__"
    master_dir = tmp_path / "master"

    data_dir.mkdir(parents=True)
    master_dir.mkdir()

    # CSVデータ作成
    csv_path = data_dir / "data.csv"
    pd.DataFrame({"x": [1, 2, 3]}).to_csv(csv_path, index=False)

    # Analyzerの生成
    analyzer = Analyzer(str(tmp_path))
    analyzer._load_groups_from_vault()

    # 確認
    assert analyzer.exist_group_name("group1")
    group = analyzer.get_group("group1")
    assert "group1_waveform" in group.unit_names() or len(group.unit_names()) > 0  # 仮名対応


def test_save(sample_analyzer: Analyzer):
    sample_analyzer.save_group('group1')

    save_unit_path = sample_analyzer.get_group('group1').get_unit('unit1').path
    df = sample_analyzer.get_group('group1').get_unit('unit1').df
    save_data_dir = save_unit_path.parent

    # assertion
    assert save_unit_path.is_file() and save_unit_path.exists()
    assert save_data_dir.is_dir() and save_data_dir.exists()
    loaded_df = pd.read_csv(save_unit_path)
    assert df.equals(loaded_df)


def test_run(sample_analyzer: Analyzer):
    # 実行対象の関数（DataFrameを3倍する）
    def multiply_data(group1: dict[str, pd.DataFrame], x: int):
        df = group1["unit1"]
        new_df = df.copy()
        new_df["a"] = df["a"] * x
        return {
            "newgroup": {
                "unitX": new_df
            }
        }

    # 実行準備
    unit_factory = DefaultDataUnitFactory()
    group_factory = DefaultDataGroupFactory()
    builder = DataBuilder(unit_factory, group_factory)
    executor = Executor(builder)

    # ExecutorをAnalyzerにセット
    sample_analyzer._executor = executor

    # 実行コンテキスト
    context = ExecContext(
        func=multiply_data,
        units_selection={"group1": []},
        kwargs={"x": 3}
    )

    # 実行
    sample_analyzer.run(context)

    # 検証
    assert sample_analyzer.exist_group_name("newgroup")
    result_group = sample_analyzer.get_group("newgroup")
    assert "unitX" in result_group.unit_names()
    result_df = result_group.get_unit("unitX").df

    expected_df = sample_analyzer.get_group("group1").get_unit("unit1").df.copy()
    expected_df["a"] *= 3
    assert result_df.equals(expected_df)
# データ解析操作基盤(作成中)

このリポジトリは、複数形式（CSV, WAVなど）のデータを柔軟に読み込み・保存し、グルーピング・操作・解析までを一貫して行う データ操作のための基盤フレームワーク です。主に以下のような特徴を持ちます：

📦 データ単位（DataUnit）とグループ（DataGroup）の明確な構造化

🏗 データリポジトリ・ファクトリ・エグゼキュータによるモジュール分離

🧪 拡張可能な解析処理実行 (Analyzer.run(exec_context))

📁 フォルダ構成に基づくデータの自動読み込み

📓 Jupyterノートによる解析ログ管理

## 📁ディレクトリ構成
```
.
├── 📂 src/ # 実装コード本体
├── 🧪 tests/ # テストコード
├── 📓 notebooks/ # Jupyterノート（分析ログ）
├── 📄 docs/ # 設計資料・クラス図
├── 📁 data/ # 生データ（.gitignore対象）
├── 🛡 .gitignore # 除外設定
├── 📝 README.md # プロジェクト概要
├── 📜 CHANGELOG.md 
└── 🔧 requirements.txt # 必要pythonモジュール
```

## コア概念
- DataUnit, DataGroup
    - DataUnit: 1つのデータファイル・メタ情報（CSVやWAVなどを構造化データにし、Pandas.DataFrameの形式でもつ）
    - DataGroup: 複数のDataUnitをグループ化し、名前で管理可能な単位
- Analyzer
    - ユーザがデータを操作するためのコアクラス
    - データの自動読み込み
        - vault/ , master/以下の構造化データからDataGroup, DataUnitを作成する。
    - 実行処理はメソッドrunと、ExecContextクラスに必要なグループ名や関数をもたせ、run(exec_context: ExecContext)で委譲可能
    - 保存はsave_group(group_name)で個別に対応。
- Repository / Factory　（責務分離）
    - CSVDataRepository, WAVDataRepositoryにより、I/O処理を抽象化
    - DefaultDataUnitFactory，WavDataUnitFactoryなどにより、読み込んだデータから単位生成
    - CSVやWAV形式以外にも、柔軟なフォーマット追加が可能な設計

![コア概念のイメージ](docs/readme_materials/example_analyzer.png)

## 使い方（Usage）
このフレームワークでは、あらかじめ用意したディレクトリ構成に従ってデータを配置することで、Analyzer が自動的にデータを読み込み、加工や解析を行うことができます。
---
① ディレクトリを準備

vault/ と master/ ディレクトリを以下のように配置してください：
~~~
data/
├── vault/
│   └── bookA/
│       └── __DATA__/
│           └── file1.wav, file2.wav ...
├── master/
│   └── bookA/
│       └── __DATA__/
│           └── file1.csv, file2.csv ...
~~~
- vault：元データ（WAVやCSVなど）を置く場所
- master：整形済みデータや保存対象を置く場所
    - master直下にcsvファイルを置くことはできますが、analyzer.deleteを実行すると削除されてしまいます。
- vault/your_group/\_\_DATA\_\_ ディレクトリ内にファイルを配置
    - vault内は後述するanalyzer.deleteを行っても削除されません。そのため、生データを保管・利用するためにvault内においてください。
    - DataGroupにはパスが設定されており、後述するAnalyzer.saveを行うと、master直下のパスに保存します。
        - ただし、vault読み込みデータは自動で保存されます。
        
---
② Analyzerを起動
~~~python
import sys
sys.path.append(os.path.abspath("/home/ymd/program/python/analyzer/src")) # 環境変数にこのパスが追加されていない場合
from cores.analyzer import Analyzer
analyzer = Analyzer(root_directory_str="./data") # Analyzerの起動には、①で作成したデータディレクトリの指定が必要
~~~
---
③データの確認・アクセス
~~~python
# グループ（本棚）の一覧
print(analyzer.group_names())

# 特定グループを取得（非推奨）
group = analyzer.get_group("bookA")

# グループ内のユニット（本）情報を確認 (非推奨)
for unit_name, unit in group.units.items():
    print(unit_name, unit.df.shape)
~~~
④処理の実行

以下の手順で実行することで、指定したDataGroupを用いて関数を実行することができます。

また、特定の返り値を返す関数の場合、その返り値を用いて新規DataGroupを作成することができます。
~~~python
# ---
# 関数の実行のみ
# ---
import pandas as pd
import sys
sys.path.append(os.path.abspath("/home/ymd/program/python/analyzer/src")) # 環境変数にこのパスが追加されていない場合
from cores.analyzer import Analyzer
from src.cores.executor.exec_context import ExecContext
# 独自関数の定義
def test1(your_selected_group_name: dict[str, pd.DataFrame], sample_number : int)
    """
    your codes
    """
    return

exec_context = {
    func = test1,
    units_selection = { # 指定したいgroup名をkeyに設定する
        "your_selected_group_name":
            [ 'book1', 'book2' ] # [None]ですべてを指定することが可能
    },
    kwargs = {sample_number: 1} # Group以外の関数の引数の明示
}

analyzer.run(exec_context)
~~~
- 活用例
    - 使用したいデータのPlotをしたいとき。
~~~python
# ---
# Groupを新規に作成したいとき
# ---
...
def test1(your_selected_group_name: dict[str, pd.DataFrame], sample_number : int)
    """
    your codes
    """
    # 返り値をdict[str, dict[str, pd.DataFrame]]で指定
    ## これを元に、新たなデータフレームが作成される
    return {'new_group_1': {'new_unit_1': new_df_1, 'new_unit_2': new_df_2}, ...}
...
~~~
- 活用例
    - 返り値をつかって新たなDataGroupを作成し、次の処理に利用したいとき
~~~python
# あたらしいgroupを作成後は以下のように保存処理をする必要がある
analyzer.save('new_group_1')
# 作成したgroupを削除したい場合は、
analyzer.delete_group('your_group_name')
~~~
---
- 全体のルール
    - Groupを作るときは返り値の型は、**dict[str, dict[str, pd.DataFrame]]**にしなくてはいけない
        - 新たなDataGroup名は、既存のものと重複してはいけない。
        - 同一のDataGroupに格納するDataUnitには、同じ名前を付けることはできない。
    - 関数で指定する引数は、ExecContextにも格納しなければいけない
        - エラーチェックを行うため。
        - 特に、引数で指定するGroup名は、実際のGroup名でなければいけない。
        - また、DataUnitを選択する際は、実際のDataUnit名でなければいけない。
        - kwargs引数を入れたい場合は、関数に「sample_number」のように指定しなくてはならず、**kwargsは利用できない。 
---
## HELP
1. DataGroup名を取得する方法は？
    - analyzer.group_names()
        - すべてのanalyzerにロードされている。
    - analyzer.print()
        - すべてのanalyzerにロードされているグループ情報を出力する。
        - ただし、引数にDataGroup名を入力することで、そのDataGroupの情報を出力する。

---
## 展望
このデータ解析基盤は今後、以下のような機能拡張や運用方法を視野に入れて進化していく予定です：

🔌 API化

Jupyter Notebook や 他のアプリケーションから HTTP 経由で Analyzer にアクセスできるようにし、非同期なデータ処理や遠隔実行を可能にする。

例：FastAPI等を活用し、run() のバックエンド化など。

🛢 SQLとの接続（Repository I/Oの拡張）

DataRepositoryの保存先・読み込み元として、CSVやWAVだけでなく RDB（MySQL / SQLite）などのSQLデータベース を扱えるようにする。

これにより、生データの保管や履歴管理、分析対象データのクエリ抽出が柔軟に行えるようになる。

🧱 依存注入(DI)の整備

ファクトリやリポジトリを外部から注入可能にし、テスト容易性や再利用性を強化する。

📊 解析関数の標準化とテンプレート化

ユーザ定義関数のフォーマットやチェック機構を拡充し、だれでも安全に run() 実行できる環境を整備する。

🧠 ノートブックの自動化・履歴管理

実行ログやパラメータを記録し、いつ・どの関数で・どんな処理がされたかを履歴として残す仕組みを導入予定。
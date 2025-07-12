# 📜 CHANGELOG

すべての変更履歴を記録するファイル。  
このプロジェクトは [セマンティック バージョニング](https://semver.org/lang/ja/) に従ってバージョン管理されます。

---
## template
```
---
## [version] - 2025-
### 🚀 追加
- （ここに次回リリース予定の機能・変更内容を書く）

---
### 🐛 修正
-
```
---
## [0.0.19-dev] - 2025-07-12
### 🚀 追加
- DataBuilderInterface
    - 関数実行時に必要
    - group_to_dict
        - DataGroup, DataUnitからdataFrameを取り出して，dict[DataGroup.name, dict[DataUnit.name, DataFrame]]にデータ形式を変更する．
    - dict_to_group
        - 関数実行時に生成されたdictをlist[DataGroup]に変換する．その後，analyzerではanalyzer.groupsに追加処理を行う．
- DataBuilder
    - concrete 
    - implemented DataBuilderInterface
    - test
        - tests/cores/test_data_builder.py

---
## [0.0.18-dev] - 2025-07-12
### 🐛 修正
- DataFactoryInterfaceに_create_methodの追加
---
## [0.0.17-dev] - 2025-07-12
### 🚀 追加
- ExecContextの修正
---
## [0.0.16-dev] - 2025-07-04
### 🚀 追加
- ExecContext
    - file:cores.exec_context.py
    - ユーザがAnalyzerに関数と指定したグループを渡して新たなDataGroup群を作る際に必要となる。
        - その際にAnalyzerに渡す引数の一部になる
    - また、渡す関数の引数に、操作したいGroup群units_selectionに格納されているGroup名とkwargsが明示されていないとエラーになる。ここでのkwargsはExecContextの引数のことであり、**kwargsのことではない。
        - **kwargsは関数に指定するとエラーが出るようにしてある。
        - あくまで明示的な関数のみを対象とした。
            - データ操作の可読性を高めるため。
---
## [0.0.15-dev] - 2025-07-02
### 🚀 追加
- analyzer.save_groupの追加
    - 指定したgroupを保存する
- dataunit
    - インターフェース DataUnitInterface, 具象　DataUnitにpathメソッドの追加
        - メタ情報のpathを返す。
        - analyzer.save追加に伴い実装。
---
### 🐛 修正
- analyzer.save_group追加のため、テストtest_analyzer.pyにtest_saveを追加


---
## [0.0.14-dev] - 2025-06-29
### 🐛 修正
- Analyzerにload系メソッドの追加とinitの整備
    - _load_units
    - _load_units_single
        - あるパスのデータを読み込んでlist[DataUnit]にする
    - _load_group
        - 読み込んだUnitリストを用いてgroupをAnalyzerの_groupに登録
    - _load_groups_from_master
        - 変換済み構造化データの読み込み
    - _load_groups_from_vault
        - 未変換のデータを変換し、master下のgroupとして作成。
        - ただし、masterに存在するものは置換しない
        - 生データ置き場
    - _load_missing_path
        - masterにvaultと同様のフォルダがあるが、読み込まれていないファイルを見つけ、ロードするメソッド

- group
    - add_unitを追加

- WavDataUnitFactoryの修正
    - WAVの２次元データにも対応できるように

-　test_analyzer.py, test_datagroup.pyのテスト
---
## [0.0.13-dev] - 2025-06-29
### 🚀 追加
- DataGroupFactoryInterfaceの実装
    - DataGroupのインスタンスを作成するクラスのインターフェース
        - create
            - units: List[DataUnitInterface]
            - name : str
            - path : Path
            - -> DataGroupInterface
- DefaultDataGroupFactoryの実装
    - 基本的なDataGroupのインスタンスを作成する具象クラス
        - create
        - _create_meta
            - name : str
            - path : Path

---
### 🐛 修正
- DataGroupの修正
    - 内部でDataUnitを用いていたものをDataUnitInterfaceに変更
---
## [0.0.12-dev] - 2025-06-29
### 🚀 追加
- WavDataRepositoryの実装
    - scipyのwavfile.readを用いて読み込む
---
### 🐛 修正
- DataRepositoryInterfaceとBaseDataRepositoryのloadメソッドはpd.DataFrameではなく、objectを返すように
    - Wavファイルを読み込むとnp.ndarrayやint形式のデータが得られるため
    - FactoryでDataFrameを作成するため、ここでは責務分離を行う
---
## [0.0.11-dev] - 2025-06-29
### 🚀 追加
- DefaultDataUnitFactory
    - create
        - DataFrame形式のデータを使ってDataUnitの配列を返す。
            - abstract: BaseDataUnitFactory
            - Defaultの場合は配列の長さが１だが、他の読み込みパターンによっては複数のDataUnitができるため、統一して配列を返すようにしている。
- WavDataUnitFactory
    - create
        - Tuple[int, np.ndarray]形式の音声データを使って、長さ２のデータフレームに。
            - int : サンプリングレート情報を格納するDataFrameに
            - np.ndarray : 波形情報をDataFrameに

---
### 🐛 修正
- DataUnitFactoryInterfaceとBaseDataUnitFactoryのcreateの返り値の型をList[DataFrame]に
- create の引数rawdataの型をobjectに変更
---
## [0.0.10-dev] - 2025-06-28
### 🚀 追加
- DataUnitFactoryInterfaceの実装
    - file: interface/dataunit_factory_interface.py
    - method
        - create
            - 生データを読み込んでDataFrameに変換し、それをDataUnitに
        - _create_meta
            - create内で使う。metaクラスの作成メソッド
- BaseDataUnitFactoryの実装
    - _create_metaはすべてのconcreteクラスで同じ処理なのでここで定義
    - test: test_base_dataunit_factory

---
## [0.0.9-dev] - 2025-06-28
### 🚀 追加
- DataGroupMetaの実装
    - implements: MetaInterface
    - file: cores/datagroup_meta.py
    - 説明　DataGroup用のMetaデータクラス
    - フィールド
        - MetaInterfaceと同じ
    - テスト
        - file: tests/cores/metas/test_datagroup_meta.py
---
### 🐛 修正
- DataGroupInterfaceの修正
    - file: interface/datafroup_interface.py
    - 説明 
        - with_update_nameの導入
- DataGroupの修正
    - file: cores/datagroup.py
    - 説明
        - _name, _pathの削除
            - DataGroupMetaへ　
        - DataGroupMetaの導入
        - with_update_nameの導入
            - meta.nameフィールドの変更ができるように
    - テスト
        - file: tests/cores/test_datagroup.py
- DataUnitの修正
    - with_update_dfの削除
        - ユーザ側にとっては不必要な操作のため
    - with_update_metaの削除
        - ユーザ側にとっては不必要な操作のため
- DataUnitMetaの修正
    - created_atを引数として与えないとき、現在時刻で設定するように
    - Pathを空文字で渡した場合ValueErrorを出すように
- 上記に合うように
    - test_datagroupを変更
---
## [0.0.8-dev] - 2025-06-28
### 🚀 追加
- MetaInterfaceの実装
    - file: interfaces/meta_interface.py
    - 説明　Metaデータ用インターフェース
    - フィールド
        - name 名前 str
        - path データ保存パス Pathオブジェクト
        - created_at 日付 datetimeオブジェクト, Optional
- DataUnitMetaの実装
    - implements: MetaInterface
    - file: cores/metas/dataunit_meta.py 
    - 説明　DataUnit用のMetaデータクラス
    - フィールド
        - format データフォーマット　str, Optional
    - テスト
        - file: tests/cores/metas/test_dataunit_meta.py

### 🐛 修正
- DataUnitの修正
    - file: cores/dataunit.py
    - DataUnitの導入
        - フィールド　_nameの削除
        - フィールド　_metadataを辞書型からDataUnitMeta型に変更
        - プロパティ　nameの削除
        - プロパティ　metadataの変更
        - メソッド　with_update_nameの変更
        - メソッド　with_update_metadataの変更
    - テスト
        file: tests/cores/test_dataunit.py
---
## [0.0.7-dev] - 2025-06-23
### 🚀 追加
DataReposityの実装とテスト
- interface: DataRepository 追加
    - file: interfaces/data_repository.py
    - save
        - DataFrameを保存する
    - load
        - DataFrameをファイルから読み込む
- Abstract: BaseDataRepository 追加
    - file: cores/base_data_repository.py
    - _ensure_path_exists
        - ファイルの保存先にディレクトリがなければ追加する
- concrete: CSVDataRepository
    - file: cores/CSVDataRepository.py
    - test: test_csv_repositoty.py
---
## [0.0.6-dev] - 2025-06-23
### 🐛 修正
- DataUnit, DataGroup, Analyzerのインターフェース名を変更
    - BaseXxx->XxxInterface
    - ファイル名
        - base_xxx.py->xxx_interface.py
---
## [0.0.5-dev] - 2025-06-22
### 🚀 追加
- DataGroupの集合体であるAnalyzerの実装とテスト
    - Interface: BaseAnalyzer
    - 各Groupにつけられた名前でアクセス可能な辞書型構造
    - exist_group_name
        - 結びつけられた名前のグループが存在しているかどうか
    - getter
        - root_dhirectory
    - delete_group
        - 指定したグループを削除
    - get_group
        - 指定した名前のグループを返す
    - _add_group
        - 新たなグループを追加する（private）
    - save_group
        -　指定したグループをファイルに保存する
---
## [0.0.4-dev] - 2025-06-22
### 🚀 追加
- DataUnitの集合体であるDataGroupの実装とテスト
    - Interface: BaseDataGroup
    - 各Unitに名前でアクセス可能な辞書型構造
    - 結びつけられた名前の存在可否メソッド
        - exist_unit_name
    - getter
        - get_unit, unit_names, units, name, path
    - DataGroupのユニット取得・例外処理に関するユニットテストを追加
    - setterは、Analyzer（未実装）での明示的なDataGroupの削除後、ユーザが渡す関数内で明示的に作成しようとしなければならない仕様（未実装）であるため、作成しない。
---
## [0.0.3-dev] - 2025-06-22
### 🚀 追加
- 最小単位のDataUnitの実装とテスト
    - Interface: BaseDataUnit

---
## [0.0.2-dev] - 2025-06-22
### 🚀 追加
- requirements.txtの更新
- test用環境の作成
    - requirements-dev.txtに必要moduleの記載
---
## [0.0.1-dev] - 2025-06-22
### 🚀 追加
- クラス図`docs/class_diagram.puml`の変更
    - 基本クラス構造の追加
---
## [0.0.0-dev] - 2025-06-22
### 🚀 追加
- CHANGELOG.mdの追加
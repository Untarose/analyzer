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
## [0.0.10] - 2025-6-28
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
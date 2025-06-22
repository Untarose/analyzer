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
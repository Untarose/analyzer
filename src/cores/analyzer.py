from abc import abstractmethod
from pathlib import Path
from interfaces.analyzer_interface import AnalyzerInterface
from cores.csv_data_repository import CSVDataRepository
from cores.wav_data_repository import WavDataRepository
from cores.default_dataunit_factory import DefaultDataUnitFactory
from cores.wav_dataunit_factory import WavDataUnitFactory
from cores.default_datagroup_factory import DefaultDataGroupFactory
from interfaces.dataunit_interface import DataUnitInterface
from interfaces.datagroup_interface import DataGroupInterface
from interfaces.data_repository_interface import DataRepositoryInterface
from interfaces.datagroup_factory_interface import DataGroupFactoryInterface
from interfaces.dataunit_factory_interface import DataUnitFactoryInterface
class Analyzer(AnalyzerInterface):
    _groups: dict[str, DataGroupInterface]
    _root_directory: Path
    _repositories: dict[str, DataRepositoryInterface]
    _dataunit_factories: dict[str, DataUnitFactoryInterface]
    _datagroup_factories: dict[str, DataGroupFactoryInterface]
    _dataunit_handlers: dict[str, tuple[DataRepositoryInterface, DataUnitFactoryInterface]]

    '''def __init__(self, groups: dict[str, DataGroupInterface], root_directory: Path) -> None:
        self._groups = groups
        self._root_directory = root_directory'''
    
    def __init__(self, root_directory_str: str) -> None:
        self._root_directory = Path(root_directory_str).resolve()
        self._groups = {}
        # directory: vault, Masterがあるかどうか
        ## なかったらエラー
        self._check_directory_requirements()

        # 各種外部クラスの集約
        '''------------------------------------------------------------------'''
        '''以下は多くなってきたらDependenciesパターンを使って外部クラスで作り直す'''
        # _repositoriesの設定
        self._repositories = {
            'csv': CSVDataRepository(),
            'wav': WavDataRepository()
        }
        #_dataunit_factoriesの設定
        self._dataunit_factories = {
            'default': DefaultDataUnitFactory(),
            'wav': WavDataUnitFactory()
        }

        # dataunit_handlersの設定
        self._dataunit_handlers = {
            "csv": (self._repositories['csv'], self._dataunit_factories['default']),
            "wav": (self._repositories['wav'], self._dataunit_factories['wav'])
        }

        #_datagroup_factoriesの設定
        self._datagroup_factories = {
            'default': DefaultDataGroupFactory()
        }
        '''------------------------------------------------------------------'''

        # masterの読み込み
        self._load_groups_from_master()
        # vaultの読み込み
        self._load_groups_from_vault()
    
                
    @property
    def root_directory(self) -> Path:
        return self._root_directory

    def group_names(self) -> list[str]:
        return list(self._groups.keys())

    def delete_group(self, group_name: str) -> None:
        if not self.exist_group_name(group_name):
            raise ValueError(f"Group '{group_name}' does not exist.")
        del self._groups[group_name]
        # TODO: ディレクトリ/ファイルの削除処理も後日実装

    def get_group(self, group_name: str) -> DataGroupInterface:
        if self.exist_group_name(group_name):
            return self._groups[group_name]
        else:
            raise ValueError(f"Group {group_name} does not exist")
        
    def _add_group(self, new_group: DataGroupInterface) -> None:
        if self.exist_group_name(new_group.name):
            raise ValueError(f"DataGroup '{new_group.name}' already exists.")
        self._groups[new_group.name] = new_group
            

    def exist_group_name(self, group_name: str) -> bool:
        return group_name in self._groups

    def save_group(self, group_name: str) -> None:
        if not self.exist_group_name(group_name):
            raise ValueError(f"Group {group_name} does not exist")
        for unit in self.get_group(group_name).units.values():
            self._repositories['csv'].save(
                unit.path,
                unit.df
            )

    
    def _check_directory_requirements(self):
        vault_path = self._root_directory / 'vault'
        if not vault_path.exists() or not vault_path.is_dir():
            print(f'[Error] "vault" directory not found in: {self._root_directory}')
            print('Please create a "vault" directory and place your original data inside it.')
            raise FileNotFoundError(f'Missing reqired directory: {vault_path}')
        
        master_path = self._root_directory / 'master'
        if not master_path.exists() or not master_path.is_dir():
            print(f'[Error] "master" directory not found in: {self._root_directory}')
            print('Please create a "master" directory and place your original data inside it.')
            raise FileNotFoundError(f'Missing reqired directory: {master_path}')
    
    def _validate_group_not_exists(self, group_name) -> None:
        if self.exist_group_name(group_name):
            raise ValueError(f'{self.__class__.__name__}: DataGroup "{group_name}" already exists')
        
    def _can_handle_ext(self, ext: str) -> bool:
        return ext in self._dataunit_handlers

    def _validate_ext(self, ext: str) -> None:
        if not self._can_handle_ext(ext):
            raise ValueError(
                f"Unsupported file extension: '{ext}'. "
                f"Supported extensions are: {list(self._dataunit_handlers.keys())}"
            )
        
#-------------------------
# 読み込み用メソッド
#-------------------------
    
    def _load_units(self, data_dir: Path, meta_path: Path) -> list[DataUnitInterface]:
            data_files = [
                file for file in data_dir.iterdir()
                    if file.is_file()
                ]
            all_units = []
            for data_path in data_files:
                name = data_path.stem
                meta_data_path = meta_path / name
                all_units += self._load_units_single(name, data_path, meta_data_path)
            return all_units

    def _load_units_single(self, name: str, data_path: Path, meta_path:Path) -> list[DataUnitInterface]:
        # 拡張子の取得
        ext = data_path.suffix[1:]
        # 拡張子が対応しているか
        ## 対応していたら特に何もなし
        self._validate_ext(ext)
        raw_data = self._dataunit_handlers[ext][0].load(data_path)
        units = self._dataunit_handlers[ext][1].create(raw_data=raw_data, name=name, path=meta_path)
        return units

    def _load_group(self, units: list[DataUnitInterface], name:str,  path: Path) -> DataGroupInterface:
        return self._datagroup_factories['default'].create(units, name, path)

    def _load_groups_from_master(self) -> None:
        # TODO　定義し終わったらtestの変更！
        # Master_directoryを読み込む
        master_path = self._root_directory / 'master'
        path_under_master = [
            path for path in master_path.rglob("*")
            if path.is_dir() and not path.name == "__DATA__"
        ]
        for path in path_under_master:
            print(path)
            # groupの名前はデータがあるディレクトリの名前
            group_name = path.name
            # もしすでにあるディレクトリ名はエラーを出す
            self._validate_group_not_exists(group_name)
            # unitのロード
            units = self._load_units(path, path)
            # groupのロード
            group = self._load_group(units, group_name, path)
            # _groupsにセット
            self._add_group(group)

    def _load_missing_path(self, group_name: str, vault_group_path: Path, master_group_path: Path) -> None:
        vault_data_dir = vault_group_path / '__DATA__'
        master_data_dir = master_group_path / '__DATA__'
        
        if not vault_data_dir.exists() or not vault_data_dir.is_dir():
            return  # データが存在しないなら何もしない

        group = self.get_group(group_name)

        for raw_file in vault_data_dir.iterdir():
            if not raw_file.is_file():
                continue

            ext = raw_file.suffix[1:]
            self._validate_ext(ext)
            repository, factory = self._dataunit_handlers[ext]
            raw_data = repository.load(raw_file)

            # unitのpathはmaster_data_dirをメタとする
            units = factory.create(raw_data=raw_data, name=group_name, path=master_data_dir)

            for unit in units:
                if not group.exist_unit_name(unit.name):
                    group.add_unit(unit)


    def _load_groups_from_vault(self) -> None:
        vault_root = self._root_directory / 'vault'
        master_root = self._root_directory / 'master'

        # __DATA__ ディレクトリをもつ group ディレクトリを探す
        vault_group_dirs = [
            data_dir.parent for data_dir in vault_root.rglob('__DATA__') if data_dir.is_dir()
        ]

        for vault_group_dir in vault_group_dirs:
            group_name = vault_group_dir.name if not vault_group_dir.name == 'vault' else 'master'
            vault_data_dir = vault_group_dir / '__DATA__'
            master_group_dir = master_root / vault_group_dir.relative_to(vault_root)
            master_data_dir = master_group_dir / '__DATA__'

            if self.exist_group_name(group_name):
                # 既存グループ → 足りないデータだけ追加
                self._load_missing_path(
                    group_name=group_name,
                    vault_group_path=vault_group_dir,
                    master_group_path=master_group_dir
                )
            else:
                # まだないグループはすべてのデータが対象
                self._validate_group_not_exists(group_name)
                units = self._load_units(vault_data_dir, master_data_dir)
                group = self._load_group(units, group_name, master_group_dir)
                self._add_group(group)
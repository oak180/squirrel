from pprint import pprint
from pathlib import Path
from typing import Self, Any
from abc import ABC, abstractmethod

import yaml

from .validate import AssetTemplate


class MissingAssetFieldError(ValueError):
    pass


class AbstractAsset(ABC):
    def __init__(self, content: dict[str, str | Any]) -> None:
        self.content = content
        return

    @property
    @abstractmethod
    def catalog_id(self) -> str:
        pass

    def as_dict(self) -> dict:
        return self.content

    def validate_fields(self, mandatory_fields: list) -> bool:
        for each_field in mandatory_fields:
            if each_field not in self.content.keys():
                raise MissingAssetFieldError(f'{each_field} missing')

        return True


class AbstractAssetCatalog(ABC):
    def __init__(self, asset_name: str, asset_catalog: dict[str, str | Any]) -> None:
        self.asset_name = asset_name
        self._asset_catalog = asset_catalog
        return

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.asset_name}, {self.asset_catalog})'

    def __str__(self) -> str:
        return f'{self.asset_name}\n' + '\n'.join(
            [name for name in self.asset_catalog.keys()]
        )

    @property
    @abstractmethod
    def asset_catalog(self) -> dict[str, AbstractAsset]:
        pass

    def as_dict(self) -> dict[str, str | Any]:
        return {self.asset_name: self.asset_catalog}

    @classmethod
    def from_file(cls, catalog_path: str) -> Self:
        catalog_file: Path = Path(catalog_path)

        if not catalog_file.name.endswith('.catalog.yaml'):
            raise ValueError('Not a template:', catalog_file.as_posix())
        if not catalog_file.exists():
            raise ValueError('No template at', catalog_file.as_posix())

        catalog_name = catalog_file.name.split('.', 1).pop(0)
        with open(catalog_file, 'r') as catalog_fp:
            catalog_dict = yaml.safe_load(catalog_fp)

        return cls(catalog_name, catalog_dict)

    def validate_catalog(self) -> bool:
        rt = True

        template: AssetTemplate = AssetTemplate.by_catalog(self.asset_name)
        mandatory_fields = template.mandatory_fields

        print(f'Validating {self.asset_name} catalog...')

        for id, asset in self.asset_catalog.items():
            print(f'Validating {id}...', end=' ')

            try:
                asset.validate_fields(mandatory_fields)
                print('Passed')
            except MissingAssetFieldError as maferr:
                print('Failed:', maferr)
                rt = False

        print('Catalog valid:', rt)
        
        return rt


if __name__ == '__main__':
    pass

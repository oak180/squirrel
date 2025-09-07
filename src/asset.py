from pathlib import Path
from typing import Self, Any
from abc import ABC, abstractmethod

import yaml

from .validate import AssetTemplate


class MissingAssetFieldError(ValueError):
    pass


class AbstractAsset(ABC):
    """
    Represents a generic asset entry
    in a generic asset catalog

    Attributes:
        `content`: the keys specified in the OpenMRS WS API
        docs and their appropriate values
    """

    def __init__(self, content: dict[str, str | Any]) -> None:
        self.content = content
        return

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.content})'

    def __str__(self) -> str:
        return f'{self.catalog_id}'

    @property
    def asset_uuid(self) -> str:
        return self.content.get('uuid')

    @property
    def display_id(self) -> str | None:
        return self.content.get('display') or None

    @property
    def catalog_id(self) -> str:
        """
        The Catalog ID for the asset
        """
        return self.display_id if self.display_id else self.asset_uuid

    def as_dict(self) -> dict:
        return self.content

    def validate_fields(self, mandatory_fields: list) -> bool:
        """
        Checks whether all `mandatory_fields` are
        present in `self.content`
        
        Returns:
            `true` if successful
        
        Raises:
            `MissingAssetFieldError` if a field \
            is found to be missing
        """
        for each_field in mandatory_fields:
            if each_field not in self.content.keys():
                raise MissingAssetFieldError(f'{each_field} missing')

        return True


class AbstractAssetCatalog(ABC):
    """
    Represents a generic asset catalog

    Attributes:
        `asset_name`: as referred to in the OpenMRS WS API docs
        `asset_catalog`: a dictionary of Catalog ID and asset attributes
    """

    def __init__(self, asset_name: str, asset_catalog: dict[str, str | Any]) -> None:
        self.asset_name = asset_name
        self._asset_catalog = asset_catalog
        return

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.asset_name}, list[{self.asset_catalog[0].__class__.__name__}])'

    def __str__(self) -> str:
        return f'{self.asset_name}: ' + ', '.join(
            [a.catalog_id for a in self.asset_catalog]
        )

    @property
    @abstractmethod
    def asset_catalog(self) -> list[AbstractAsset]:
        """
        Instantiates a dictionary of Catalog IDs and `Asset`(s)
        from the catalog
        """
        return [AbstractAsset(a) for a in self._asset_catalog.values()]

    def as_dict(self) -> dict[str, str | Any]:
        return {
            self.asset_name: {a.catalog_id: a.as_dict() for a in self.asset_catalog}
        }

    @classmethod
    def from_file(cls, catalog_path: str) -> Self:
        """
        Instantiates an Asset Catalog from file
        
        Arguments:
            `catalog_path`: the path to a \
            `name.catalog.yaml` file where the `name` \
            matches the `asset_name`
        """
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

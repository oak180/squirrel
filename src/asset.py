from pathlib import Path
from typing import Self, Any, Literal
from abc import ABC, abstractmethod

import yaml
import csv
import requests

from .env_vars import ASSETS, WS_URI, WS_AUTH
from .ws import WSResponseHandler

class MissingAssetFieldError(ValueError):
    pass


class AbstractAsset(ABC):
    """
    Represents a generic asset entry

    Arguments:
        `content`:
            the keys specified in the OpenMRS docs and
            their appropriate values

    Attributes:
        `catalog_id`:
            the index in the asset catalog

    Methods:
        `as_dict`:
            returns a dictionary of key-value pairs as per
            OpenMRS WS API docs
    """

    def __init__(self, content: dict[str, str | Any]) -> None:
        self.content = content
        return

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.content})'

    def __str__(self) -> str:
        return f'{self.catalog_id}'

    @property
    @abstractmethod
    def catalog_id(self) -> str:
        if id := self.content.get('display'):
            return id
        else:
            return self.content.get('uuid')

    def as_dict(self) -> dict:
        return self.content

    def validate_fields(self, mandatory_fields: list) -> bool:
        """
        Checks whether all `mandatory_fields` are
        present in `self.content`

        Returns:
            `true`:
                if successful

        Raises:
            `MissingAssetFieldError`:
                if a field is found to be missing
        """
        for each_field in mandatory_fields:
            if each_field not in self.content.keys():
                raise MissingAssetFieldError(f'{each_field} missing')

        return True


class AbstractAssetCatalog(ABC):
    """
    Represents an asset catalog

    Arguments:
        `catalog_name`:
            as referred to in the OpenMRS WS API docs (e.g., "user")
        `asset_catalog`:
            a dictionary of Catalog ID and asset content

    Methods:
        `asset_catalog`:
            Returns the catalog IDs of assets within this catalog
        `as_dict`:
            returns a dictionary of catalog IDs and content of assets
        `from_file`:
            constructs an asset catalog from YAML file
        `to_file`:
            exports the catalog to `ASSETS/catalog_name.catalog.yaml`
    """

    def __init__(self, catalog_name: str, asset_catalog: dict[str, str | Any]) -> None:
        self.catalog_name = catalog_name
        self._post_init(asset_catalog)
        return

    @abstractmethod
    def _post_init(self, asset_catalog: dict[str, str | Any]) -> None:
        self._asset_catalog = [
            AbstractAsset(a) for a in asset_catalog.values()
        ]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.catalog_name}, list[{self.asset_catalog[0].__class__.__name__}])'

    def __str__(self) -> str:
        return f'{self.catalog_name}: {self.asset_catalog}'

    @property
    def asset_catalog(self) -> list[AbstractAsset]:
        return [str(a) for a in self._asset_catalog]

    def as_dict(self) -> dict[str, str | Any]:
        return {
            a.catalog_id: a.as_dict() for a in self._asset_catalog
        }

    @classmethod
    def from_file(cls, catalog_name: str, catalog_path: str | None = None) -> Self:
        """
        Instantiates an Asset Catalog from file

        Arguments:
            `catalog_name`:
                the type of the resource within the catalog, like `user`
            `catalog_path`:
                the path to a `*.catalog.yaml` file

        If only `catalog_name` is given, the AssetCatalog is instantiated
        from `ASSETS/catalog_name.catalog.yaml`.

        If both `catalog_name` and `catalog_path` are given, the AssetCatalog is
        instantiated from `catalog_path`
        """

        # removed this from the docstring as 
        # we're ignoring templates for a while
        # " and the validation is as per `TEMPLATES/catalog_name.template.yaml`"

        if not catalog_path:
            catalog_path = '/'.join([ASSETS, f'{catalog_name}.catalog.yaml'])
        elif not catalog_path.endswith('.catalog.yaml'):
            raise ValueError('Not a catalog:', catalog_path)

        catalog_file = Path(catalog_path)

        if not catalog_file.exists():
            raise ValueError('No catalog at:', catalog_file.as_posix())

        with open(catalog_file, 'r') as catalog_fp:
            catalog_dict = yaml.safe_load(catalog_fp)

        return cls(catalog_name, catalog_dict)
    
    @classmethod
    @abstractmethod
    def _nester(cls, asset_content: dict[str, str | Any]) -> dict [str, str | Any]:
        return asset_content
    
    @classmethod
    def from_csv(cls, catalog_name: str, key_col: str, catalog_path: str | None = None) -> Self:
        
        if not catalog_path:
            catalog_path = '/'.join([ASSETS, f'{catalog_name}.catalog.csv'])
        elif not catalog_path.endswith('.catalog.csv'):
            raise ValueError('Not a catalog:', catalog_path)
        
        catalog_file = Path(catalog_path)

        if not catalog_file.exists():
            raise ValueError('No catalog at:', catalog_path)
        
        catalog_dict = {}
        
        with open(catalog_file, 'r') as catalog_fp:
            reader = csv.DictReader(catalog_fp)
            for row in reader:
                key = row[key_col]
                catalog_dict[key] = cls._nester(row)

        return cls(catalog_name, catalog_dict)
    
    @classmethod
    def fetch_resources(
        cls,
        endpoint: str,
        uuid: str | None = None,
        delete: False | Literal['retire', 'purge'] = False
    ) -> Any:

        scheme = WS_URI + f'/{endpoint}'

        if uuid:
            scheme += f'/{uuid}'

        if delete:
            if not uuid:
                raise ValueError('No UUID to delete')
            if delete == 'purge':
                scheme += '?purge=true'
            if delete not in ['retire', 'purge']:
                raise ValueError('Invalid delete mode')
            
            r = requests.delete(scheme, auth = WS_AUTH)

        else:
            r = requests.get(scheme , auth = WS_AUTH)
        
        response = WSResponseHandler(r)
        response.write_data()

        return
        
        # RESPONSE CODES
        # 200: GET worked
        # 204: DELETE worked
            # if '?purge=true' is not appended, the resource is just voided (Retired = true)
        # 401: Unauthorized
        # 404: Not found

    @classmethod
    def purge_all_resources(cls, endpoint: str) -> Any:
        raise NotImplementedError('thinking about it')

    @abstractmethod
    def load_resources(self, endpoint: str) -> dict:
        
        scheme = WS_URI + f'/{endpoint}'
        responses = []

        for a in self._asset_catalog:
            r = requests.post(scheme, json=a.as_dict(), auth=WS_AUTH)
            responses.append(WSResponseHandler(r))

        return responses




    def to_file(self, catalog_path: str = None) -> None:
        
        if not catalog_path:
            catalog_path = '/'.join(
                [ASSETS, f'{self.catalog_name}.catalog.yaml']
            )
        elif not catalog_path.endswith('.catalog.yaml'):
            raise ValueError('Not a catalog:', catalog_path)
        
        with open(catalog_path, 'w') as catalog_fp:
            yaml.dump(self.as_dict(), catalog_fp)

        return None


if __name__ == '__main__':
    pass

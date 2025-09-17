from abc import ABC, abstractmethod
from typing import Any, Self, Literal, Type
from pathlib import Path
from pprint import pprint

import requests
import csv

from .env_vars import WS_URI, WS_AUTH, OUTPUT, ASSETS
from .ws import WSResponseHandler

class AbstractAsset(ABC):
    def __init__(self, content: dict[str, Any]) -> None:
        self._content = content
        return
    
    def __str__(self) -> str:
        return self.catalog_id
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.content})'
    
    @property
    def content(self) -> dict[str, Any]:
        return self._content
    
    @property
    @abstractmethod
    def catalog_id(self) -> str:
        """The unique catalog index for this asset"""
        raise NotImplementedError

    @abstractmethod
    def nester(self) -> dict[str, Any]:
        """The mapping as per WS API docs for this asset"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def endpoint(cls) -> str:
        """The endpoint as per WS API docs"""
        raise NotImplementedError

    @property
    def uuid(self) -> str:
        """The auto-generated UUID (if updated)"""
        return self.content.get('uuid', None)
    
    @classmethod
    @abstractmethod
    def fieldnames(cls) -> list[str]:
        """The fieldnames to write as rows"""
        raise NotImplementedError

    @classmethod
    def flattener(cls, nested_mapping: dict[str, Any]) -> dict[str, str]:
        """Returns the flattened mapping from nested object"""
        return {f:nested_mapping.get(f) for f in cls.fieldnames()}
    
    @classmethod
    def fetch_resource(cls, uuid: str) -> Self:
        
        scheme = f'{WS_URI}/{cls.endpoint()}/{uuid}'
        response = requests.get(scheme, auth=WS_AUTH)
        handler = WSResponseHandler(response, output=True) # TODO fetch_resource: set output to False
        content = handler.content
        flat_content = cls.flattener(content)

        return cls(flat_content)



class AssetCatalog:
    def __init__(self, assets: list[AbstractAsset]) -> None:
        self.assets = assets
        self.asset_class = type(self.assets[0])
        return
    
    def __str__(self) -> str:
        members = ', '.join([str(a) for a in self.assets])
        return f'{self.catalog_name}: {members}'
    
    @property
    def catalog_name(self) -> str:
        """Returns the catalog name, usually matching the resource name"""
        return self.asset_class.endpoint

    @staticmethod
    def _io_path(env_location: str, name: str, path: str | None = None, create: bool = False) -> Path:

        if not path:
            path = f'{env_location}/{name}.catalog.csv'
        elif not path.endswith('.catalog.csv'):
            raise ValueError(f'Not a catalog: {path}')
        
        file = Path(path)
        if not file.exists():
            if create:
                file.touch()
            else:
                raise ValueError(f'No catalog at {file.as_posix()}')
        
        return file
    
    @classmethod
    def from_fetch(cls, asset_class: Type[AbstractAsset]) -> Self:

        scheme = f'{WS_URI}/{asset_class.endpoint()}'
        response = requests.get(scheme, auth=WS_AUTH)
        handler = WSResponseHandler(response)
        results = handler.content.get('results')
        uuids = [each.get('uuid') for each in results]
        assets = [asset_class.fetch_resource(u) for u in uuids]
        
        return cls(assets)

    @classmethod
    def from_csv(cls, csv_name: str, asset_class: Type[AbstractAsset]) -> Self:

        csv_file = cls._io_path(ASSETS, csv_name)
        assets = []

        with open(csv_file, 'r') as csv_fp:
            reader = csv.DictReader(csv_fp)

            for each_row in reader:
                a = asset_class(each_row)
                assets.append(a)

        return cls(assets)

    def to_csv(self, csv_name: str, ) -> None:

        csv_file = self._io_path(OUTPUT, csv_name, create=True)

        with open(csv_file, 'w') as csv_fp:
            a = self.assets[0]
            writer = csv.DictWriter(csv_fp, a.fieldnames())
            writer.writeheader()

            for each in self.assets:
                writer.writerow(each.content)

        return None
    
    def to_post(self) -> None:
        
        scheme = f'{WS_URI}/{self.catalog_name}'

        for each in self.assets:
            payload = each.nester()
            response = requests.post(scheme, data=payload, auth=WS_AUTH)
            _ = WSResponseHandler(response)

        return None

    @abstractmethod
    def delete_resources(self) -> None:

        scheme = f'{WS_URI}/{self.asset_class.endpoint}'

        for each in self.assets:
            scheme += f'/{each.uuid}'
            response = requests.delete(scheme, auth=WS_AUTH)
            _ = WSResponseHandler(response)

        return None

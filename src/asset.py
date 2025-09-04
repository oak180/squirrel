from pprint import pprint
from pathlib import Path
from typing import Self

import yaml

from .validate import AssetTemplate


class AssetCatalog:
    def __init__(self, asset_name: str, asset_catalog: list[dict]) -> None:
        self.asset_name = asset_name
        self.assets_list = [
            Asset(a) for a in asset_catalog
        ]
        return

    def prettify(self) -> None:
        for each in self.assets_list:
            each.prettify()
        return

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

    def validate_catalog(self) -> None:

        template: AssetTemplate = AssetTemplate.by_catalog(self.asset_name)
        mandatory_fields = template.mandatory_fields

        for each_asset in self.assets_list:
            try:
                each_asset.validate_fields(mandatory_fields)
                print('validated')
            except Exception as e:
                print(e)

        return None


class Asset:
    def __init__(self, content: dict) -> None:
        self.content = content
        return

    def prettify(self) -> None:
        pprint(self.content)
        return

    def as_dict(self) -> dict: return self.content

    def validate_fields(self, mandatory_fields: list) -> None:

        for each_field in mandatory_fields:
            if each_field not in self.content.keys():
                raise ValueError(f'missing field: {each_field}')

        return None


if __name__ == "__main__":
    pass
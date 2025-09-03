from pathlib import Path
from typing import Any, Self
from pprint import pprint

import yaml


OWAIS = {
        'username': 'owais',
        'password': 'OwaisKh1',
        'systemId': 'owais.khan',
        'person': {
            'gender': 'M',
            'birthdate': '1993-10-07',
            'names': [
                {
                    'givenName': 'Owais',
                    'familyName': 'Khan'
                }
            ],
            'addresses': [
                {
                    'address1': 'B-23, St. 1, KUECHS',
                    'address2': 'Gulzar-e-Hijri Scheme 33',
                    'cityVillage': 'Karachi',
                    'stateProvince': 'Sindh',
                    'country': 'Pakistan'
                }
            ]
        }
    }


class AssetCatalog:
    def __init__(self, asset_name: str, asset_catalog: list[dict]) -> None:
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



class Asset:
    def __init__(self, asset_dict: dict) -> None:
        self.asset_dict = asset_dict
        return
    
    def prettify(self) -> None:
        pprint(self.asset_dict)
        return


class _AssetTemplateField:
    def __init__(self, name: str, props: dict) -> None:
        self.name = name
        self.props = props

        if ('type' in self.props) and ('desc' in self.props):
            self.type = self.props.get('type')
            self.desc = self.props.get('desc')
        else:
            raise ValueError(f'type and/or desc missing in {self.name}')
        
        self.is_mandatory = self.props.setdefault('mandatory', False)
        self.is_required = self.props.setdefault('required', False)

        return
    
    def __repr__(self) -> str:
        s = f'{self.name} | {self.desc} | {self.type}'

        if self.is_mandatory:
            s += ' | mandatory'.upper()
        if self.is_required:
            s += ' | required'.upper()

        return s
    

class AssetTemplate:
    def __init__(self, name: str, content: dict) -> None:
        self.name = name
        self.props = content.get('props')
        self.is_subresource = self.props.get('subresource')

        self.fields = [
            _AssetTemplateField(k, v) for k, v in content.get('fields').items()
        ]

        return
    
    def prettify(self) -> None:
        print('Template for asset:', self.name)
        print('Is Subresource:', self.is_subresource)
        for each_field in self.fields:
            print(each_field)
        return
    
    def __repr__(self) -> str:
        return f'{self.name} | Is subresource: {'Y' if self.is_subresource else 'N'}'

    @classmethod
    def from_file(cls, template_path: str) -> Self:

        template_file: Path = Path(template_path)

        if not template_file.name.endswith('.template.yaml'):
            raise ValueError('Not a template:', template_file.as_posix())
        if not template_file.exists():
            raise ValueError('No template at', template_file.as_posix())
        
        template_name = template_file.name.split('.', 1).pop(0)
        with open(template_file, 'r') as template_fp:
            template_dict = yaml.safe_load(template_fp)

        return cls(template_name, template_dict)

    def list_required_fields(self) -> None:
        for f in self.fields:
            if f.is_required:
                print(f.name)


def validate_asset() -> None:

    template: AssetTemplate = AssetTemplate.from_file(
        r'/home/user/Projects/squirrel/data/templates/user.template.yaml'
    )

    catalog: AssetCatalog = AssetCatalog.from_file(
        r'/home/user/Projects/squirrel/data/assets/user.catalog.yaml'
    )

    catalog.prettify()

    return


if __name__ == "__main__":
    pass
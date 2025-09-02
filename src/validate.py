from pathlib import Path
from typing import Any, Self
from pprint import pprint

import yaml



def load_asset() -> dict[str, Any]:

    user_asset = {
        'username': 'owais',
        'password': 'OwaisKh1',
        'systemId': 'owais.khan',
        'person': {
            'gender': 'M',
            'birthDate': '1993-10-07',
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

    return user_asset




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
        for each_field in self.list_fields():
            print(each_field)
        return
    
    def __repr__(self) -> str:
        return self.content

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

    def list_fields(self) -> list:
        return self.fields




def validate_asset(template_path: Path) -> None:

    validator: AssetTemplate = AssetTemplate.from_file(template_path)
    asset = load_asset()

    validator.prettify()
    # print(asset)



    return

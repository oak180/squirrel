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




class _TemplateField:
    def __init__(self, template_field: dict) -> None:
        self.template_field = template_field
        self.field_name = list(self.template_field.keys())[0]
        self.field_props = self.template_field.get(self.field_name)
        self.field_type = self.field_props.get('type')
        self.field_desc = self.field_props.get('desc')
        self.is_mandatory = self.field_props.setdefault('mandatory', False)
        self.is_required = self.field_props.setdefault('required', False)
        return
    
    def __repr__(self) -> str:
        s = f'{self.field_name} ({self.field_type}): {self.field_desc}'

        if self.is_mandatory:
            s += ' (mandatory)'
        if self.is_required:
            s += ' (required)'

        return s
    
    def prettify(self) -> None:
        pprint(self.template_field)
        return
    



class Template:
    def __init__(self, template_dict: dict) -> None:
        self.template_dict = template_dict
        self.template_fields = [
            _TemplateField(f) for f in self.template_dict.get('fields')
        ]
        return
    
    def prettify(self) -> None:
        pprint(self.template_dict)
        return
    
    def __repr__(self) -> str:
        return self.template_dict

    @classmethod
    def from_file(cls, template_path: str) -> Self:

        template_file: Path = Path(template_path)

        if not template_file.exists():
            raise ValueError('No template at', template_file.as_posix())
        
        with open(template_file, 'r') as template_fp:
            template = yaml.safe_load(template_fp)

        return cls(template)

    def list_fields(self) -> list:
        return self.template_fields




def validate_asset(template_path: Path) -> None:

    validator: Template = Template.from_file(template_path)
    asset = load_asset()

    validator.prettify()
    ls_fields = validator.list_fields()

    print(type(ls_fields[0]))

    for each_field in ls_fields:
        print(each_field)
    # print(asset)



    return

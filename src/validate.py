from pathlib import Path
from typing import Any, Self
from pprint import pprint

import yaml


def load_template(template_file: Path) -> dict[str, Any]:

    with open(template_file, 'r') as template_fp:
        template: dict = yaml.safe_load(template_fp)

    return template


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


class Template:
    def __init__(self, template: dict) -> None:
        self.template = template
        return
    
    def prettify(self) -> None:
        pprint(self.template)
        return
    
    def __repr__(self) -> None:
        return self.template

    @classmethod
    def from_file(cls, template_path: str) -> Self:

        template_file: Path = Path(template_path)

        if not template_file.exists():
            raise ValueError('No template at', template_file.as_posix())
        
        with open(template_file, 'r') as template_fp:
            template = yaml.safe_load(template_fp)

        return cls(template)
        



def validate_asset(template_path: Path) -> None:

    validator: Template = Template.from_file(template_path)
    asset = load_asset()

    validator.prettify()
    print(asset)



    return

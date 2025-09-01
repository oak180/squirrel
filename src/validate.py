from pathlib import Path
from typing import Any

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


def validate_asset(template_path: Path) -> None:

    template = load_template(template_path)
    asset = load_asset()

    print(template)
    print(asset)

    return

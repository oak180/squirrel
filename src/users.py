from typing import Any, Self

import requests

from .env_vars import WS_URI, WS_AUTH
from .sys_paths import handle_write, can_write
from .asset import AbstractAsset, AbstractAssetCatalog


class UserAsset(AbstractAsset):
    def __init__(self, content):
        super().__init__(content)
        return
    
    @property
    def catalog_id(self) -> str:
        return self.content.get('systemId')
    
    
class UserAssetCatalog(AbstractAssetCatalog):
    def __init__(self, catalog_name, asset_catalog):
        super().__init__(catalog_name, asset_catalog)
        return
    
    def _post_init(self, asset_catalog):
        self._asset_catalog = [
            UserAsset(a) for a in asset_catalog.values()
        ]
        return

    @classmethod
    def _nester(cls, asset_content: dict[str, str | Any]) -> dict[str, str | Any]:

        return {
            'username': asset_content.get('username'),
            'password': asset_content.get('password'),
            'systemId': asset_content.get('systemId'),
            'person': {
                'gender': asset_content.get('gender'),
                'names': [
                    {
                        'givenName': asset_content.get('givenName'),
                        'familyName': asset_content.get('familyName')
                    }
                ]
            }
        }
    
    @classmethod
    def from_csv(cls, catalog_name = 'user', key_col = 'systemId', catalog_path = None):
        return super().from_csv(catalog_name, key_col, catalog_path)
    
    @classmethod
    def fetch_resources(cls, endpoint = 'user', uuid = None, purge = False):
        return super().fetch_resources(endpoint, uuid, purge)
    
    def load_resources(self, endpoint = 'user'):
        return super().load_resources(endpoint)

"""
Functions to be implemented as methods
"""

def extract_users(target_path: str, overwrite: bool = False) -> None:
    target_file = can_write(target_path, overwrite=overwrite)

    pull_resp = requests.get(WS_URI + '/user', auth=WS_AUTH)
    if not pull_resp.status_code == 200:
        raise requests.ConnectionError(
            f'Status Code {pull_resp.status_code}: {pull_resp.json()}'
        )

    try:
        handle_write(pull_resp.json(), target_file)
        print(f'Wrote users to {target_file.name}')
    except Exception as e:
        print(f'Write failed: {e}')

    return None


def delete_user(target_uuid: str) -> None:
    del_resp = requests.delete(WS_URI + f'/user/{target_uuid}?purge=true', auth=WS_AUTH)
    if not del_resp.status_code == 204:
        raise requests.ConnectionError(f'{del_resp.status_code}: {del_resp.json()}')

    return None


def input_user(user_data: dict) -> str:
    user_resp = requests.post(WS_URI + '/user', json=user_data, auth=WS_AUTH)
    if not user_resp.status_code == 201:
        return f'Input User failed: {user_resp.json().get("error").get("message")}'

    return f'Input User successful: {user_resp.json().get("systemId")}'


if __name__ == '__main__':
    pass

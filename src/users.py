from typing import Any

import requests

from .env_vars import WS_URI, WS_AUTH
from .sys_paths import handle_write, can_write
from .asset import AbstractAsset, AbstractAssetCatalog


class UserAsset(AbstractAsset):
    """
    Inherits from `AbstractAsset` and adds
    further functionality to manage users in OpenMRS
    """
    def __init__(self, content: dict[str, str | Any]) -> None:
        super().__init__(content)
        return

    @property
    def catalog_id(self) -> str:
        return self.content.get('systemId')

class UserAssetCatalog(AbstractAssetCatalog):
    def __init__(self, asset_name, asset_catalog) -> None:
        super().__init__(asset_name, asset_catalog)

    @property
    def asset_catalog(self) -> list[UserAsset]:
        return [UserAsset(a) for a in self._asset_catalog.values()]

    @staticmethod
    def fetch_users() -> requests.Response:
        """
        Successful status code is 200
        """
        return requests.get(WS_URI + '/user/82f18b44-6814-11e8-923f-e9a88dcb533f', auth = WS_AUTH)

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

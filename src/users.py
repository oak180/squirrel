from typing import Any, Self

import requests
import logging

from .env_vars import WS_URI, WS_AUTH
from .sys_paths import handle_write, can_write
from .catalog import AbstractAsset, AssetCatalog


class UserAsset(AbstractAsset):
    def __init__(self, content):
        super().__init__(content)
        return
    
    @property
    def catalog_id(self) -> str:
        return self.content.get('systemId')
    
    @property
    def nester(self) -> dict[str, Any]:
        d = {
            'username': self.content.get('username'),
            'systemId': self.content.get('systemId'),
            'person': {
                'gender': self.content.get('gender'),
                'names': [
                    {
                        'givenName': self.content.get('givenName'),
                        'familyName': self.content.get('familyName')
                    }
                ]
            }
        }

        pw = input(f'Password for {d.get('systemId')}')
        if len(pw) < 8:
            raise ValueError('Password must be 8 or more characters')
        else:
            d['password'] = pw
            return d
    
    @classmethod
    def endpoint(cls):
        return 'user'

    @classmethod
    def fieldnames(cls) -> list[str]:
        return ['username', 'systemId', 'givenName', 'familyName', 'gender']
    
    

if __name__ == '__main__':
    pass

from pprint import pprint
from pathlib import Path
import logging
import requests
import yaml

from src.env_vars import WS_URI, WS_AUTH, ASSETS, OUTPUT, LOGS
from src.users import UserAsset
from src.ws import WSResponseHandler
from src.catalog import AssetCatalog

WRITE_PATH = r'/home/user/Projects/squirrel/data/assets/fetched.catalog.yaml'

def main():
    pprint('hello from squirrel')

    users: AssetCatalog = AssetCatalog.from_fetch(UserAsset)
    
    users.to_csv('user')
    
    # FIXME Catalog.from_fetch
    # continue by validating the loaded resources
    # in src/assets.py, or in src/users.py?

    pprint('bye from squirrel')

    return


if __name__ == '__main__':

    logging.basicConfig(
    filename=f'{LOGS}/squirrel.log',
    level=logging.INFO
    )

    main()

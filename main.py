from pprint import pprint
from pathlib import Path
import logging
import requests
import yaml

from src.env_vars import WS_URI, WS_AUTH, ASSETS, OUTPUT, LOGS
from src.users import UserAssetCatalog
from src.ws import WSResponseHandler

WRITE_PATH = r'/home/user/Projects/squirrel/data/assets/fetched.catalog.yaml'

def main():
    pprint('hello from squirrel')

    

    users = UserAssetCatalog.from_file('user')

    user_load: list[WSResponseHandler] = users.load_resources()

    stdout = [each.data for each in user_load]

    with open(f'{OUTPUT}/user_load.yaml', 'w') as fp:
        yaml.dump(stdout, fp)
    
    # todo implement (reasonable) abstraction
    # todo 
    # todo write unit tests
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

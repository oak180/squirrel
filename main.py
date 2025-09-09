from pprint import pprint
from pathlib import Path
import requests
import yaml

from src.env_vars import WS_URI, WS_AUTH, ASSETS, OUTPUT
from src.users import UserAssetCatalog

WRITE_PATH = r'/home/user/Projects/squirrel/data/assets/fetched.catalog.yaml'

def main():
    pprint('hello from squirrel')

    users = UserAssetCatalog.from_csv()

    r = users.load_resources('user')

    with open(f'{OUTPUT}/user_load.yaml', 'w') as fp:
        yaml.dump(r, fp)

    r = users.fetch_resources()

    with open(f'{OUTPUT}/user_fetch.yaml', 'w') as fp:
        yaml.dump(r, fp)
    
    # todo implement (reasonable) abstraction
    # todo 
    # todo write unit tests
    # continue by validating the loaded resources
    # in src/assets.py, or in src/users.py?

    return


if __name__ == '__main__':
    main()

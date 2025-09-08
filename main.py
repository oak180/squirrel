from pprint import pprint
from pathlib import Path
import requests
import yaml

from src.env_vars import WS_URI, WS_AUTH

WRITE_PATH = r'/home/user/Projects/squirrel/data/assets/fetched.catalog.yaml'
FETCHED_USERS: dict = {"results":[{"uuid":"82f18b44-6814-11e8-923f-e9a88dcb533f","display":"admin","links":[{"rel":"self","uri":"http://localhost:8080/openmrs/ws/rest/v1/user/82f18b44-6814-11e8-923f-e9a88dcb533f","resourceAlias":"user"}]},{"uuid":"ad89e996-0146-4951-a0be-75876dc50781","display":"javeria","links":[{"rel":"self","uri":"http://localhost:8080/openmrs/ws/rest/v1/user/ad89e996-0146-4951-a0be-75876dc50781","resourceAlias":"user"}]},{"uuid":"87ad4b89-8ca2-40b7-b828-edf483d04f56","display":"owais","links":[{"rel":"self","uri":"http://localhost:8080/openmrs/ws/rest/v1/user/87ad4b89-8ca2-40b7-b828-edf483d04f56","resourceAlias":"user"}]}]}

def main():
    pprint('hello from squirrel')

    fetched_names = {a.get('display'):a.get('uuid') for a in FETCHED_USERS.get('results')}

    fetched_assets = dict()

    for k, v in fetched_names.items():

        r = requests.get(WS_URI + f'/user/{v}', auth = WS_AUTH)

        if r.status_code == 200:
            fetched_assets[k] = r.json()
            print(k, 'fetched')
        else:
            fetched_assets[k] = None
            print(k, 'failed')

    write_file = Path(WRITE_PATH)
    with open(write_file, 'w') as write_fp:
        yaml.dump(fetched_assets, write_fp)

    pprint(fetched_names)

    # todo implement (reasonable) abstraction
    # todo 
    # todo write unit tests
    # continue by validating the loaded resources
    # in src/assets.py, or in src/users.py?

    return


if __name__ == '__main__':
    main()

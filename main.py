from pprint import pprint

from src import AbstractAssetCatalog
from src.users import UserAssetCatalog

CATALOG = r'/home/user/Projects/squirrel/data/assets/user.catalog.yaml'

def main():
    pprint('hello from squirrel')

    cat = UserAssetCatalog.from_file(CATALOG)
    print(cat)
    print(f'{repr(cat)=}')

    print(', '.join([str(a) for a in cat.asset_catalog]))

    # r = UserAssetCatalog.fetch_users()

    # pprint(r.status_code)
    # pprint(r.headers)
    # pprint(r.json())

    # todo implement (reasonable) abstraction
    # todo 
    # todo write unit tests
    # continue by validating the loaded resources
    # in src/assets.py, or in src/users.py?

    return


if __name__ == '__main__':
    main()

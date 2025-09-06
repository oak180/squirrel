from pprint import pprint

from src import AbstractAssetCatalog
from src.users import UserAssetCatalog

def main():
    pprint('hello from squirrel')

    cat: UserAssetCatalog = UserAssetCatalog.from_file(
        r'/home/user/Projects/squirrel/data/assets/user.catalog.yaml'
    )

    cv = cat.validate_catalog()

    if cv:
        print('cat happy =)')
    else:
        print('cat sad =(')

    # todo implement (reasonable) abstraction
    # todo 
    # todo write unit tests
    # continue by validating the loaded resources
    # in src/assets.py, or in src/users.py?

    return


if __name__ == '__main__':
    main()

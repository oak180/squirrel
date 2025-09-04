from pprint import pprint

from src import AssetCatalog


def main():
    pprint('hello from squirrel')

    cat: AssetCatalog = AssetCatalog.from_file(
        r'/home/user/Projects/squirrel/data/assets/user.catalog.yaml'
    )

    print('Status:', cat.validate_catalog())

    # todo implement (reasonable) abstraction
    # todo 
    # todo write unit tests
    # continue by validating the loaded resources
    # in src/assets.py, or in src/users.py?

    return


if __name__ == '__main__':
    main()

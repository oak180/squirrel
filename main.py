from pprint import pprint

from src.users import extract_users, delete_user, input_user
from src.assets import load_assets

def main():
    print('hello from squirrel')

    resources = load_assets('user')
    pprint(resources)

    # todo refactor: 'dictionary' -> 'asset'
    # todo
    #  validate loaded assets
    # continue by validating the loaded resources
    # in src/assets.py, or in src/users.py?

    return


if __name__ == '__main__':
    main()

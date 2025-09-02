from pprint import pprint

from src.users import extract_users, delete_user, input_user
from src import validate_asset, Template

from src.sys_paths import TEMPLATES

def main():
    print('hello from squirrel')

    asset = 'user'
    kind = 'template'
    ext = 'yaml'

    template_path = list(TEMPLATES.glob(
        f'{asset}.{kind}.{ext}'
    ))
    print('Template:', template_path)

    if len(template_path) == 1:
        validate_asset(template_path[0])


    # todo write unit tests
    # todo validate one asset
    # continue by validating the loaded resources
    # in src/assets.py, or in src/users.py?

    return


if __name__ == '__main__':
    main()

from pprint import pprint

from src.users import extract_users, delete_user, input_user
from src.dictionaries import load_dictionary

def main():
    print('hello from squirrel')

    resources = load_dictionary('user')
    pprint(resources)

    # continue by validating the loaded resources
    # in src/dictionaries.py, or in src/users.py?
    # refactoring? dictionaries vs resources (to avoid confusion)

    return


if __name__ == '__main__':
    main()

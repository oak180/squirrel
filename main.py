from dotenv import load_dotenv
from pathlib import Path
import requests
import os
import yaml

from src.users import extract_users, delete_user, input_user


def input_user_dir(input_path: str) -> tuple[str, str]:
    input_file = Path(input_path)
    if not input_file.suffix == '.yaml':
        raise ValueError(f'{input_file.name} is not in YAML format')
    if not input_file.exists() or not input_file.is_file():
        raise FileNotFoundError(f'{input_file.name} not found')

    with open(input_file, 'r') as users_fp:
        user_dir = yaml.full_load(users_fp)

    added = []
    failed = []
    for each_user in user_dir.get('users'):
        user_resp = input_user(each_user)
        if user_resp.status_code == 201:
            added.append(each_user.get('username'))
        elif user_resp.status_code == 500:
            failed.append(
                f'{user_resp.status_code} | {each_user.get("error").get("message")}'
            )
        else:
            print(user_resp.status_code, user_resp.json(), sep='\n')
            failed.append(
                f'{user_resp.status_code} | {each_user.get("username")} | {user_resp.json().get("message")}'
            )

    return f'Added: {", ".join(added)}', f'Failed: {", ".join(failed)}'


def main():
    print('hello from squirrel')

    payload = {
        'username': 'zaeem',
        'password': 'ZaeemKh1',
        'systemId': 'zaeem.khan',
        'person': {
            'gender': 'M',
            'names': [{'givenName': 'Zaeem', 'familyName': 'Khan'}],
        },
    }

    job_res = input_user(payload)
    print(job_res)

    extract_users('remaining.users.dictionary.yaml', overwrite=True)

    return


if __name__ == '__main__':
    main()

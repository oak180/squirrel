from dotenv import load_dotenv
from pathlib import Path
import requests
import os
import yaml


def extract_users(output_path: str) -> tuple[int, str]:
    output_file = Path(output_path)
    if output_file.exists():
        raise FileExistsError(f'{output_file.name} already exists')

    users_resp = requests.get(ws_uri + '/user', auth=ws_auth)
    if not users_resp.status_code == 200:
        return (users_resp.status_code, users_resp.json().get('message'))

    users_dir = users_resp.json()
    user_list = [x.get('display') for x in users_dir.get('results')]

    with open(output_file, 'w') as output_fp:
        yaml.dump(users_dir, output_fp)

    return (users_resp.status_code, f'Extracted: {", ".join(user_list)}')


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


def input_user(user_data: dict) -> tuple[int, str]:
    user_resp = requests.post(ws_uri + '/user', json=user_data, auth=ws_auth)
    return user_resp


def delete_user(target_uuid: str) -> tuple[int, str]:
    del_resp = requests.delete(ws_uri + f'/user/{target_uuid}?purge=true', auth=ws_auth)
    if del_resp.status_code == 200:
        return del_resp.status_code, del_resp.json()
    elif del_resp.status_code == 500:
        return del_resp.status_code, del_resp.json().get('error').get('message')
    else:
        return del_resp.status_code, del_resp


def main():
    print('hello from squirrel')

    job = extract_users(r'./data_files/users.out.dictionary.yaml')
    print(job)

    return


if __name__ == '__main__':
    load_dotenv()

    ws_uri = os.getenv('WS_URI')
    ws_user = os.getenv('WS_USER')
    ws_pass = os.getenv('WS_PASS')
    ws_auth = (ws_user, ws_pass)

    main()

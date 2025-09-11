import requests
import yaml
import logging
import datetime

from .env_vars import OUTPUT, LOGS


class WSResponseHandler:
    """
    Handles responses from the OpenMRS WS API
    """
    def __init__(self, response: requests.Response) -> None:
        try:
            response.raise_for_status()
        except requests.HTTPError as herr:
            logging.error(f'HTTPError: {herr}')
            self.data = {
                'content_type': 'error',
                'message': response.json().get('error').get('message')
            }
            return None

        self.status_code = response.status_code
        self.reason = response.reason if response.reason else None

        self.content_type = response.headers.get('Content-Type', None)
        if not self.content_type:
            return None
        if 'application/json' in self.content_type:
            self.data = {
                'content_type': 'mapping',
                'owais': response.json()
            }
        elif 'text/plain' in self.content_type:
            self.data = {
                'content_type': 'plaintext',
                'content': response.text
            }
        else:
            self.data = {
                'content_type': 'other',
            }

        logging.info(f'{self.status_code} ({self.reason}): {self.data}')
        
        return None
    
    def write_data(self) -> None:

        now = datetime.datetime.now()
        t_string = now.strftime('%H%M')
        d_string = now.strftime('%d%m%Y')

        file_name = f'{t_string}_{d_string}_out.yaml'

        with open(f'{OUTPUT}/{file_name}', 'w') as fp:
            yaml.dump(self.data, fp)

        logging.info(f'wrote to {file_name}')

        return None

from typing import Literal, Any

import requests
import yaml
import logging
import datetime
import uuid

from .env_vars import OUTPUT


class WSResponseHandler:
    """
    Handles responses from the OpenMRS WS API
    """
    def __init__(
        self,
        response: requests.Response,
        output: bool = True
    ) -> None:
        self.status_code = response.status_code
        self.reason = response.reason if response.reason else None
        self.content_type = response.headers.get('Content-Type', None)
        self._content = None

        self.log_msg = f'{self.status_code} ({self.reason}) '

        try:
            response.raise_for_status()
        except requests.HTTPError as _:
            self.log_msg += f'| {response.json().get('error').get('message')}'
            logging.warning(self.log_msg)

        else:
            if 'application/json' in self.content_type:
                self._content = response.json()
                self.log_msg += '| Content: object'

            elif 'text/plain' in self.content_type:
                self.log_msg += f'| {response.text}'

            elif not self.content_type:
                self.log_msg += '| No content'
                pass

            else:
                self._content = response.content
                self.log_msg += '| Content: binary'
                
            logging.info(self.log_msg)

        finally:
            if self._content and output:
                self._output_content()

        return None
    
    @property
    def content(self) -> dict[str, Any]:
        if self._content:
            return self._content
        else:
            raise AttributeError('No content in response body')
    
    def _output_content(self) -> None:

        now = datetime.datetime.now()
        d_string = now.strftime('%d%m%Y')
        t_string = now.strftime('%H%M%S')
        unique = uuid.uuid4().hex[:8]
    
        file_name = f'{d_string}_{t_string}_{unique}_out.yaml'

        with open(f'{OUTPUT}/{file_name}', 'w') as fp:
            yaml.dump(self.content, fp)

        logging.info(f'output to {file_name}')

        return None

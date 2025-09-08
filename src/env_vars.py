from dotenv import load_dotenv
import os
import requests


class GetRequest:
    """
    Represents a GET Request to the OpenMRS WS API
    
    Attributes:
        `endpoint`: The endpoint of the URL (e.g., `/user` in `WS_URI+'/user'`)
    """
    
    def __init__(self, endpoint: str) -> None:
        self.uri = WS_URI + endpoint
        self.auth = WS_AUTH
        return None
    
    @property
    def response(self):
        pass


if __name__ == '__main__':
    pass
else:
    load_dotenv()

    DB_URI: str = os.getenv('DB_URI')
    WS_URI: str = os.getenv('WS_URI')
    WS_USER: str = os.getenv('WS_USER')
    WS_PASS: str = os.getenv('WS_PASS')
    WS_AUTH: tuple[str, str] = (WS_USER, WS_PASS)

    OUTPUT: str = os.getenv('OUTPUT')
    TEMPLATES: str = os.getenv('TEMPLATES')
    ASSETS: str = os.getenv('ASSETS')
    TEMPORARY: str = os.getenv('TEMPORARY')

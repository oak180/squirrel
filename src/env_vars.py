from dotenv import load_dotenv
import os


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
    DICTIONARIES: str = os.getenv('DICTIONARIES')
    TEMPORARY: str = os.getenv('TEMPORARY')

from dotenv import load_dotenv
import os

load_dotenv()

DB_URI: str = os.getenv('DB_URI')
WS_URI: str = os.getenv('WS_URI')
WS_USER: str = os.getenv('WS_USER')
WS_PASS: str = os.getenv('WS_PASS')
WS_AUTH: tuple[str, str] = (WS_USER, WS_PASS)

DATA_DIR: str = os.getenv('DATA_DIR')

if __name__ == '__main__':
    pass

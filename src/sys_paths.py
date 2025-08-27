from pathlib import Path
from typing import Any
import yaml

from .env_vars import DATA_DIR

DATA_DIR: Path = Path(DATA_DIR)


def can_write(target_path: str, overwrite: bool = False) -> Path:
    target_file: Path = DATA_DIR.joinpath(Path(target_path))
    if target_file.exists() and not overwrite:
        raise ValueError(f'{target_file.name} already exists')

    return target_file


def handle_write(response_data: Any, target_file: Path) -> None:
    with open(target_file, 'w') as target_fp:
        yaml.dump(response_data, target_fp)

    return None


if __name__ == '__main__':
    pass

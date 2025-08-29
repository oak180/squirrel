from pathlib import Path
from typing import Any, Literal
import yaml

from .env_vars import OUTPUT, TEMPLATES, DICTIONARIES, TEMPORARY


def find_source(source_name: str, source_type: Literal['dictionary', 'template']) -> Path:
    """Find appropriate dictionary by source_name"""

    if source_type == 'dictionary':
        resources = list(DICTIONARIES.glob(f'{source_name}.{source_type}.yaml'))
        if len(resources) == 1: 
            return resources[0]

    elif source_type == 'template':
        resources = list(TEMPLATES.glob(f'{source_name}.{source_type}.yaml'))
        if len(resources) == 1: 
            return resources[0]


def can_write(target_path: str, overwrite: bool = False) -> Path:
    target_file: Path = OUTPUT.joinpath(Path(target_path))
    if target_file.exists() and not overwrite:
        raise ValueError(f'{target_file.name} already exists')

    return target_file


def handle_write(response_data: Any, target_file: Path) -> None:
    with open(target_file, 'w') as target_fp:
        yaml.dump(response_data, target_fp)

    return None


if __name__ == '__main__':
    pass
else:
    OUTPUT: Path = Path(OUTPUT)
    TEMPLATES: Path = Path(TEMPLATES)
    DICTIONARIES: Path = Path(DICTIONARIES)
    TEMPORARY: Path = Path(TEMPORARY)

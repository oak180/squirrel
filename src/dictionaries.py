"""Module for validating a dictionary by template"""
# import templates and dictionaries
# check whether mandatory/required fields exist

import yaml

from .sys_paths import find_source


def load_dictionary(source_name: str) -> dict:

    source = find_source(source_name, 'dictionary')

    with open(source, 'r') as source_fp:
        resource = yaml.safe_load(source_fp)

    return resource


if __name__ == "__main__":
    pass

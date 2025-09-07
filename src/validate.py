from pathlib import Path
from typing import Any, Self
from pprint import pprint

import yaml

from .env_vars import TEMPLATES


class _AssetTemplateField:
    def __init__(self, name: str, props: dict) -> None:
        self.name = name
        self.props = props

        if ('type' in self.props) and ('desc' in self.props):
            self.type = self.props.get('type')
            self.desc = self.props.get('desc')
        else:
            raise ValueError(f'type and/or desc missing in {self.name}')
        
        self.is_mandatory = self.props.setdefault('mandatory', False)
        self.is_required = self.props.setdefault('required', False)

        return
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name}, {self.props})'
    
    def __str__(self) -> str:
        return f'Field: {self.name} ({self.type}) | {self.desc}'
    
    def as_dict(self) -> dict: return {self.name: self.props}
        

class AssetTemplate:
    def __init__(self, name: str, content: dict) -> None:
        self.name = name
        self._properties = content.get('properties')
        self.desc = self._properties.get('desc')
        self.is_subresource = self._properties.get('subresource')

        self._fields = [
            _AssetTemplateField(k, v) for k, v in content.get('fields').items()
        ]

        return
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name}, {self.properties})'
    
    def __str__(self) -> str: 
        return f'{self.name} | {self.desc}'

    @property
    def properties(self) -> dict[str, str | Any]:
        return self._properties
    
    @property
    def fields(self) -> dict[str, str | Any]:
        return {f.name:f.props for f in self._fields}
    
    @property
    def required_fields(self) -> dict[str, str | Any]:
        return {f.name:f.props for f in self._fields if f.is_required}
    
    @property
    def mandatory_fields(self) -> dict[str, str | Any]:
        return {f.name:f.props for f in self._fields if f.is_mandatory}

    def as_dict(self) -> dict:
        return {
            self.name: {
                'properties': self.properties,
                'fields': self.fields
            }
        }
    
    @staticmethod
    def by_catalog(asset_name: str) -> Self:
        
        return AssetTemplate.from_file(
            '/'.join([TEMPLATES, f'{asset_name}.template.yaml'])
        )

    @classmethod
    def from_file(cls, template_path: str) -> Self:

        if not isinstance(template_path, Path):
            template_file: Path = Path(template_path)
        else:
            template_file = template_path

        if not template_file.name.endswith('.template.yaml'):
            raise ValueError('Not a template:', template_file.as_posix())
        if not template_file.exists():
            raise ValueError('No template at', template_file.as_posix())
        
        template_name = template_file.name.split('.', 1).pop(0)
        with open(template_file, 'r') as template_fp:
            template_dict = yaml.safe_load(template_fp)

        return cls(template_name, template_dict)




if __name__ == "__main__":
    pass
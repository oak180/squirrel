

from .catalog import AbstractAsset

class RoleAsset(AbstractAsset):
    def __init__(self, content):
        super().__init__(content)
        return None
    
    @property
    def catalog_id(self):
        return self.content.get('name')
    
    def nester(self):
        return self.flattener(self.content)
        # only because "nested" mapping is also actually flat for Role
    
    @classmethod
    def flattener(cls, nested_mapping):
        return {
            'name': nested_mapping.get('name'),
            'description': nested_mapping.get('description'),
            'inheritedRoles': [
                i.get('uuid') for i in nested_mapping.get('inheritedRoles')
            ],
            'privileges': [
                i.get('uuid') for i in nested_mapping.get('privileges')
            ],
            'uuid': nested_mapping.get('uuid')
        }
    
    @classmethod
    def endpoint(cls):
        return 'role'
    
    @classmethod
    def fieldnames(cls):
        return [
            'name',
            'description',
            'inheritedRoles',
            'privileges',
            'uuid'
        ]

    def delete_resource(self):
        return super().delete_resource()

class PrivilegeAsset(AbstractAsset):
    def __init__(self, content):
        super().__init__(content)
        return
    
    @property
    def catalog_id(self):
        return self.content.get('name')
    
    def nester(self):
        return self.flattener(self.content)
        # only because "nested" mapping is also actually flat for Role

    @classmethod
    def flattener(cls, nested_mapping):
        return {
            'name': nested_mapping.get('name'),
            'description': nested_mapping.get('description'),
            'uuid': nested_mapping.get('uuid')
        }
    
    @classmethod
    def endpoint(cls):
        return 'privilege'
    
    @classmethod
    def fieldnames(cls):
        return [
            'name',
            'description',
            'uuid'
        ]
    
    def delete_resource(self):
        return super().delete_resource()
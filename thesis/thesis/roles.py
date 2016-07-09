from rolepermissions.roles import AbstractUserRole

class Moderator(AbstractUserRole):
    available_permissions = {
        'add_item': True,
    }
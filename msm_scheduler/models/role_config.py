from typing import List

class RoleConfig:
    def __init__(self, **kwargs):
        self.role_name = kwargs.get('role_name', '')
        self.classes = [c.strip() for c in kwargs.get('classes', '').split(',')] if kwargs.get('classes') else []
        self.min_hp_offset = int(kwargs.get('min_hp_offset', 0))
        self.whitelist = [p.strip() for p in kwargs.get('whitelist', '').split(',')] if kwargs.get('whitelist') else []
        self.blacklist = [p.strip() for p in kwargs.get('blacklist', '').split(',')] if kwargs.get('blacklist') else []

    @property
    def role_name(self):
        return self._role_name

    @role_name.setter
    def role_name(self, value: str):
        if not value:
            raise ValueError("Role name cannot be empty")
        self._role_name = value.lower()  # Store role names in lowercase for comparison

    @property
    def classes(self):
        return self._classes

    @classes.setter
    def classes(self, value: List[str]):
        if not all(isinstance(c, str) for c in value):
            raise ValueError("All class entries must be strings")
        self._classes = value

    @property
    def min_hp_offset(self):
        return self._min_hp_offset

    @min_hp_offset.setter
    def min_hp_offset(self, value: int):
        if value < 0:
            raise ValueError("min_hp_offset must be a positive integer")
        self._min_hp_offset = value

    @property
    def whitelist(self):
        return self._whitelist

    @whitelist.setter
    def whitelist(self, value: List[str]):
        if not all(isinstance(p, str) for p in value):
            raise ValueError("All whitelist entries must be strings")
        self._whitelist = value

    @property
    def blacklist(self):
        return self._blacklist

    @blacklist.setter
    def blacklist(self, value: List[str]):
        if not all(isinstance(p, str) for p in value):
            raise ValueError("All blacklist entries must be strings")
        self._blacklist = value

    def is_whitelisted(self, player_name: str) -> bool:
        """Check if a player is whitelisted for this role"""
        return player_name in self.whitelist

    def can_player_take_role(self, player_name: str, player_class: str, player_hp: int, boss_hp_required: int) -> bool:
        """Check if a player can take this role based on class, HP, and blacklist"""
        # Check blacklist first
        if player_name in self.blacklist:
            return False

        # For altar role, only check HP requirement
        if self.role_name == 'altar':
            return player_hp >= (boss_hp_required + self.min_hp_offset)

        # For other roles, check both class and HP
        return (player_class in self.classes and 
                player_hp >= (boss_hp_required + self.min_hp_offset)) 
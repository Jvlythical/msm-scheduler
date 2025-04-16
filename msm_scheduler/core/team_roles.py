from typing import List, Dict, Tuple
from ..models.player import Player
from ..models.boss import Boss
from ..models.role_config import RoleConfig
from ..lib.logger import Logger, bcolors

LOG_ID = 'TeamRoles'

class TeamRoles:
    def __init__(self, players: List[Player], boss: Boss, role_configs: List[RoleConfig] = None):
        self.players = players
        self.boss = boss
        self.role_configs = {rc.role_name.lower(): rc for rc in (role_configs or [])}
        self.roles: Dict[str, List[Player]] = {
            'host': [],
            'bishop': [],
            'altar': [],
            'firestorm': [],
            'fireball': []
        }
        Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}Loaded role configs: {list(self.role_configs.keys())}{bcolors.ENDC}")
        self._assign_roles()

    def _assign_roles(self):
        # Host is first player
        if self.players:
            self.roles['host'] = [self.players[0]]

        # Assign bishops
        self.roles['bishop'] = [p for p in self.players if p.player_class == 'Bishop']
        print(f"Found {len(self.roles['bishop'])} bishops")

        # Get role configs
        firestorm_config = self.role_configs.get('firestorm')
        fireball_config = self.role_configs.get('fireball')
        altar_config = self.role_configs.get('altar')

        Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}Processing firestorm candidates...{bcolors.ENDC}")
        # Assign firestorm based on config
        if firestorm_config:
            # First check whitelist - each whitelisted player gets the role
            firestorm_whitelist = []
            for p in self.players:
                if firestorm_config.is_whitelisted(p.name):
                    firestorm_whitelist.append(p)
                    Logger.instance(LOG_ID).info(f"Player {p.name} is whitelisted for firestorm role")
            
            if firestorm_whitelist:
                # If we have whitelisted players, use all of them
                self.roles['firestorm'] = firestorm_whitelist
                Logger.instance(LOG_ID).info(f"Assigned firestorm to whitelisted players: {[p.name for p in firestorm_whitelist]}")
            else:
                # Otherwise use the original logic to find the best candidate
                firestorm_candidates = []
                for p in self.players:
                    can_take_role = firestorm_config.can_player_take_role(
                        p.name, p.player_class, p.hp, self.boss.hp_required
                    )
                    Logger.instance(LOG_ID).info(
                        f"Player {p.name} (class: {p.player_class}, hp: {p.hp}) "
                        f"{'can' if can_take_role else 'cannot'} take firestorm role"
                    )
                    if can_take_role:
                        firestorm_candidates.append(p)

                if firestorm_candidates:
                    firestorm = min(firestorm_candidates, key=lambda p: p.max_damage_cap)
                    self.roles['firestorm'] = [firestorm]
                    Logger.instance(LOG_ID).info(f"Assigned firestorm to {firestorm.name}")

        Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}Processing altar candidates...{bcolors.ENDC}")
        # Assign altar roles based on config
        if altar_config:
            # First check whitelist
            altar_whitelist = []
            for p in self.players:
                if altar_config.is_whitelisted(p.name):
                    altar_whitelist.append(p)
                    Logger.instance(LOG_ID).info(f"Player {p.name} is whitelisted for altar role")
            
            # Then check other candidates who meet HP requirements
            altar_candidates = []
            for p in self.players:
                # Skip players already assigned to firestorm
                if p in self.roles['firestorm']:
                    continue
                    
                can_take_role = altar_config.can_player_take_role(
                    p.name, p.player_class, p.hp, self.boss.hp_required
                )
                Logger.instance(LOG_ID).info(
                    f"Player {p.name} (class: {p.player_class}, hp: {p.hp}, mdc: {p.max_damage_cap}) "
                    f"{'can' if can_take_role else 'cannot'} take altar role"
                )
                if can_take_role and p not in altar_whitelist:
                    altar_candidates.append(p)

            # Sort by max damage cap (lowest first)
            altar_candidates.sort(key=lambda p: p.max_damage_cap)
            Logger.instance(LOG_ID).info(f"Initial altar candidates: {[p.name for p in altar_candidates]}")
            
            # Combine whitelisted players with other candidates
            all_altar_candidates = altar_whitelist + altar_candidates
            
            # If we don't have enough altar candidates meeting HP requirements,
            # add remaining players who aren't firestorm
            if len(all_altar_candidates) < 5:
                remaining_players = [p for p in self.players 
                                   if p not in self.roles['firestorm'] and p not in all_altar_candidates]
                Logger.instance(LOG_ID).info(f"Remaining players: {[p.name for p in remaining_players]}")
                
                # Sort remaining players by max damage cap (lowest first)
                remaining_players.sort(key=lambda p: p.max_damage_cap)
                Logger.instance(LOG_ID).info(f"Sorted remaining players: {[p.name for p in remaining_players]}")
                
                # Add enough players to reach 5 altar roles
                needed = 5 - len(all_altar_candidates)
                additional_players = remaining_players[:needed]
                Logger.instance(LOG_ID).info(f"Adding {needed} additional players: {[p.name for p in additional_players]}")
                
                all_altar_candidates.extend(additional_players)
                Logger.instance(LOG_ID).info(
                    f"Not enough players meeting HP requirements for altar. "
                    f"Added {needed} additional players with lowest max damage cap."
                )
            
            Logger.instance(LOG_ID).info(f"Final altar candidates before limiting to 5: {[p.name for p in all_altar_candidates]}")
            self.roles['altar'] = all_altar_candidates[:5]
            Logger.instance(LOG_ID).info(f"Final altar roles after limiting to 5: {[p.name for p in self.roles['altar']]}")

        Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}Processing fireball candidates...{bcolors.ENDC}")
        # Assign fireball based on config
        if fireball_config:
            fireball_candidates = []
            for p in self.players:
                # Skip players already assigned to firestorm only
                if p in self.roles['firestorm']:
                    continue
                    
                # Check whitelist first
                if fireball_config.is_whitelisted(p.name):
                    fireball_candidates.append(p)
                    Logger.instance(LOG_ID).info(f"Player {p.name} is whitelisted for fireball role")
                    continue
                    
                # Otherwise check other requirements
                can_take_role = fireball_config.can_player_take_role(
                    p.name, p.player_class, p.hp, self.boss.hp_required
                )
                Logger.instance(LOG_ID).info(
                    f"Player {p.name} (class: {p.player_class}, hp: {p.hp}) "
                    f"{'can' if can_take_role else 'cannot'} take fireball role"
                )
                if can_take_role:
                    fireball_candidates.append(p)
            
            self.roles['fireball'] = fireball_candidates
            if fireball_candidates:
                Logger.instance(LOG_ID).info(f"Assigned fireball to {[p.name for p in fireball_candidates]}")

    def get_player_roles(self, player: Player) -> List[str]:
        """Returns list of roles for a player in priority order"""
        player_roles = []
        for role in ['host', 'bishop', 'altar', 'firestorm', 'fireball']:
            if player in self.roles[role]:
                player_roles.append(role.capitalize())
        return player_roles

    def get_ordered_players(self) -> List[tuple[Player, List[str]]]:
        """Returns players ordered by role priority with their roles"""
        ordered = []
        seen = set()
        
        # Order by role priority
        for role in ['host', 'bishop', 'altar', 'firestorm', 'fireball']:
            for player in self.roles[role]:
                if player not in seen:
                    seen.add(player)
                    ordered.append((player, self.get_player_roles(player)))
        
        # Add remaining players
        for player in self.players:
            if player not in seen:
                seen.add(player)
                ordered.append((player, []))
                
        return ordered 
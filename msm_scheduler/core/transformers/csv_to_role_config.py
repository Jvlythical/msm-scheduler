from typing import Dict, List

class CSVToRoleConfigTransformer:
    def __init__(self, rows):
        self.rows = rows

    def transform(self):
        role_configs = []
        for row in self.rows:
            if 'Role Name' not in row or not row['Role Name']:
                continue

            role_configs.append({
                'role_name': row['Role Name'].strip(),
                'classes': row['Classes'].strip() if row.get('Classes') else '',
                'min_hp_offset': int(row['Min HP Offset']) if row.get('Min HP Offset') else 0,
                'whitelist': row['Whitelist'].strip() if row.get('Whitelist') else '',
                'blacklist': row['Blacklist'].strip() if row.get('Blacklist') else ''
            })
        return role_configs 
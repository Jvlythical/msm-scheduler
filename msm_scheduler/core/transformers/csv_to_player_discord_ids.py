from typing import Dict, List, Iterator

class CSVToPlayerDiscordIdsTransformer():
    def __init__(self, rows):
        self.rows = rows

    def tranform(self):
        discord_ids = []
        for row in self.rows:
            if 'Identity' in row and 'Discord ID' in row:
                discord_ids.append({
                    'identity': row['Identity'].strip(),
                    'discord_id': row['Discord ID'].strip()
                })
        return discord_ids 
"""
Clan Chest
"""

import csv
import json
import os

from .base import BaseGen


class ClanChest(BaseGen):
    def __init__(self, config):
        super().__init__(config)

    def run(self):
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.clan_chest)

        thresholds = [0]
        gold = [0]
        cards = [0]

        tvt_thresholds = [0]
        tvt_gold = [0]
        tvt_cards = [0]

        field_map = {
            'CLAN_CROWN_CHEST_THRESHOLDS': thresholds,
            'CLAN_CROWN_CHEST_GOLD': gold,
            'CLAN_CROWN_CHEST_CARDS': cards,
            'CLAN_TEAM_VS_TEAM_CHEST_THRESHOLDS': tvt_thresholds,
            'CLAN_TEAM_VS_TEAM_CHEST_GOLD': tvt_gold,
            'CLAN_TEAM_VS_TEAM_CHEST_CARDS': tvt_cards
        }

        with open(csv_path, encoding="utf8") as f:
            reader = csv.DictReader(f)

            current_name = ''

            for row in reader:
                name = row["Name"]

                if len(name):
                    current_name = name

                if current_name in field_map:
                    field_map[current_name].append(int(row["NumberArray"]))

        out = {
            '1v1': {
                "thresholds": thresholds,
                "gold": gold,
                "cards": cards
            },
            '2v2': {
                "thresholds": tvt_thresholds,
                "gold": gold,
                "cards": cards
            }
        }

        json_path = os.path.join(self.config.json.base, self.config.json.clan_chest)
        with open(json_path, 'w') as f:
            json.dump(out, f, indent=4)

        print(json_path)

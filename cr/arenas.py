"""
Generate arenas JSON from APK CSV source.
"""

import csv
import json
import os

from .base import BaseGen
from .util import camelcase_split


class Arenas(BaseGen):
    def __init__(self, config):
        super().__init__(config)

    def run(self):
        """Generate rarities jsons"""
        rarities = []
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.arenas)
        fields = [
            "Name", "Arena", "ChestArena", "TvArena", "IsInUse", "TrainingCamp", "PVEArena",
            "TrophyLimit", "DemoteTrophyLimit", "SeasonTrophyReset", "ChestRewardMultiplier",
            "ShopChestRewardMultiplier", "RequestSize", "MaxDonationCountCommon", "MaxDonationCountRare",
            "MaxDonationCountEpic", "IconSWF", "IconExportName", "MainMenuIconExportName", "SmallIconExportName",
            "MatchmakingMinTrophyDelta", "MatchmakingMaxTrophyDelta", "MatchmakingMaxSeconds", "PvpLocation",
            "TeamVsTeamLocation", "DailyDonationCapacityLimit", "BattleRewardGold", "ReleaseDate", "SeasonRewardChest",
            "QuestCycle", "ForceQuestChestCycle"
        ]

        def value(v):
            if str(v).isdigit():
                return int(v)
            return v

        arenas = []
        with open(csv_path, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i > 0:
                    name = row.get('Name')
                    arena = {'_'.join(camelcase_split(k)).lower(): value(v) for k, v in row.items() if k in fields}
                    arena.update({
                        "title": self.text(row["TID"], "EN"),
                        "subtitle": self.text(row["SubtitleTID"], "EN"),
                    })
                    arenas.append(arena)

        json_path = os.path.join(self.config.json.base, self.config.json.arenas)
        with open(json_path, 'w') as f:
            json.dump(arenas, f, indent=4)

        print(json_path)

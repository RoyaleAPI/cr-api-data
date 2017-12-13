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

    def arena_key(self, row):
        """unique key of the arena. Used for image assets."""
        if int(row["Arena"]) <= 12:
            return "arena{}".format(row["Arena"])
        else:
            return "league{}".format(row["Name"][-1])

    def run(self):
        """Generate rarities jsons"""
        rarities = []
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.arenas)
        fields = [
            "Name", "Arena", "ChestArena", "TvArena", "IsInUse", "TrainingCamp", "PVEArena", "TrophyLimit",
            "DemoteTrophyLimit", "SeasonTrophyReset", "ChestRewardMultiplier", "ShopChestRewardMultiplier",
            "RequestSize", "MaxDonationCountCommon", "MaxDonationCountRare", "MaxDonationCountEpic",
            "MatchmakingMinTrophyDelta", "MatchmakingMaxTrophyDelta", "MatchmakingMaxSeconds", "PvpLocation",
            "TeamVsTeamLocation", "DailyDonationCapacityLimit", "BattleRewardGold", "ReleaseDate", "SeasonRewardChest",
            "QuestCycle", "ForceQuestChestCycle"
        ]

        def value(v):
            if str(v).isdigit():
                return int(v)
            return v

        arenas = []
        types = {}
        with open(csv_path, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    types = {k: v for k, v in row.items() if k in fields}
                if i > 0:
                    arena = {'_'.join(camelcase_split(k)).lower(): self.row_value(row, k, types) for k, v in row.items()
                             if k in fields}
                    arena.update({
                        "key": self.arena_key(row),
                        "title": self.text(row["TID"], "EN"),
                        "subtitle": self.text(row["SubtitleTID"], "EN"),
                        "arena_id": min(12, arena["arena"]),
                        "league_id": arena["name"][-1]
                    })
                    for k, v in arena.copy().items():
                        if isinstance(v, str) and v.isdigit():
                            arena[k] = int(v)

                    if arena['is_in_use']:
                        arenas.append(arena)

        arenas = sorted(arenas, key=lambda x: x["arena"])
        json_path = os.path.join(self.config.json.base, self.config.json.arenas)
        with open(json_path, 'w') as f:
            json.dump(arenas, f, indent=4)

        print(json_path)

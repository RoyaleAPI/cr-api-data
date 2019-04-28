"""
Generate arenas JSON from APK CSV source.
"""

import csv
import os

from .base import BaseGen
from .util import camelcase_split


class Arenas(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="arenas", null_int=True)

    def arena_key(self, row):
        """unique key of the arena. Used for image assets."""
        if int(row["Arena"]) <= 12:
            return "arena{}".format(row["Arena"])
        else:
            return "league{}".format(row["Name"][-1])

    def run(self):
        """Generate json"""
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.arenas)
        fields = [
            "Name", "Arena", "ChestArena", "TvArena", "IsInUse", "TrainingCamp", "TrophyLimit", "DemoteTrophyLimit",
            "SeasonTrophyReset", "ChestRewardMultiplier", "ShopChestRewardMultiplier", "RequestSize",
            "MaxDonationCountCommon", "MaxDonationCountRare", "MaxDonationCountEpic", "MatchmakingMinTrophyDelta",
            "MatchmakingMaxTrophyDelta", "MatchmakingMaxSeconds", "DailyDonationCapacityLimit", "BattleRewardGold",
            "SeasonRewardChest", "QuestCycle", "ForceQuestChestCycle"]

        arenas = []

        with open(csv_path, encoding="utf8") as f:
            reader = csv.DictReader(f)
            sc_id = 0

            for i, row in enumerate(reader):
                if i > 0:
                    # skip rows with no names
                    if not row.get('Name'):
                        continue

                    arena = {'_'.join(camelcase_split(k)).lower(): self.row_value(row, k) for k, v in row.items()
                             if k in fields}
                    arena_id = min(12, arena["arena"])
                    league_id = max(0, arena['arena'] - 12)

                    arena.update({
                        "key": self.arena_key(row),
                        "title": self.text(row["TID"], "EN"),
                        "subtitle": self.text(row["SubtitleTID"], "EN"),
                        "arena_id": arena_id,
                        "league_id": league_id,
                        # "id": 54000000 + i - 1
                        "id": 54000000 + sc_id
                    })
                    for k, v in arena.copy().items():
                        if isinstance(v, str) and v.isdigit():
                            arena[k] = int(v)

                    if arena['is_in_use']:
                        arenas.append(arena)

                    sc_id += 1

        arenas = sorted(arenas, key=lambda x: x["arena"])

        json_path = os.path.join(self.config.json.base, self.config.json.arenas)
        self.save_json(arenas, json_path)

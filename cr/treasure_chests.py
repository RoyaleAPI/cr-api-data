"""
Treasure chests generator
"""
import csv

from .base import BaseGen
from .util import camelcase_split


class TreasureChests(BaseGen):

    def __init__(self, config):
        super().__init__(config, id="treasure_chests")

        self.fields = ["Name", "BaseChest", "Arena", "InShop", "InArenaInfo", "TournamentChest", "SurvivalChest",
                       "ShopPriceWithoutSpeedUp", "TimeTakenDays", "TimeTakenHours", "TimeTakenMinutes",
                       "TimeTakenSeconds", "RandomSpells", "DifferentSpells", "ChestCountInChestCycle", "RareChance",
                       "EpicChance", "LegendaryChance", "SkinChance", "GuaranteedSpells", "MinGoldPerCard",
                       "MaxGoldPerCard", "DescriptionTID", "TID", "NotificationTID", "SpellSet", "Exp", "SortValue",
                       "SpecialOffer", "DraftChest", "BoostedChest", "LegendaryOverrideChance"
                       ]

        self.base_chests = []
        self.items = []

    def get_base_chest_stats(self, name):
        """Return base chest stats as dict."""
        props = [
            "time_taken_hours", "time_taken_minutes", "time_taken_seconds",
            "random_spells", "different_spells",
            "chest_count_in_chest_cycle",
            "rare_chance", "epic_chance", "legendary_chance", "skin_chance",
            "min_gold_per_card", "max_gold_per_card"
        ]
        for item in self.items:
            if name == item["name"]:
                return {k: v for k, v in item.items() if k in props}
        return {}

    def run(self):
        """Generate treasure chests."""
        with open(self.csv_path, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i > 0:
                    item = {'_'.join(camelcase_split(k)).lower(): self.row_value(row, k) for k, v in row.items()
                             if k in self.fields}

                    if item.get("base_chest"):
                        item.update(self.get_base_chest_stats(item["base_chest"]))

                    self.items.append(item)

        # items = sorted(self.items, key=lambda x: str(x["name"]))
        self.save_json(self.items, self.json_path)



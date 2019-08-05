"""
Treasure chests generator (v2)
"""
from csv2json import read_csv
from .base import BaseGen


class TreasureChests(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="treasure_chests", null_int=True)

    def run(self):
        """Generate json."""
        rows = read_csv(self.csv_path)

        for index, row in enumerate(rows):
            row.update({
                "name_en": self.text(row.get('tid'), "EN"),
                "notification": self.text(row.get("notification_tid"), "EN"),
            })

        self.save_json(rows)
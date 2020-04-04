"""
Generate rarities JSON from APK CSV source.
"""

import os

from csv2json import read_csv
from .base import BaseGen


class DraftDeck(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="draft_deck")

    def run(self):
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.draft_deck)
        rows = read_csv(csv_path)
        rows = self.value_dict_to_list(rows)





        json_path = os.path.join(self.config.json.base, self.config.json.draft_deck)
        self.save_json(rows, json_path)

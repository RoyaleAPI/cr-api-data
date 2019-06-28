"""
Generate predefined decks JSON from APK CSV source.
"""

import os

from csv2json import read_csv
from .base import BaseGen


class PredefinedDecks(BaseGen):
    def __init__(self, config):
        super().__init__(config)

    def run(self):
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.predefined_decks)
        rows = read_csv(csv_path)
        rows = self.value_dict_to_list(rows)
        rows = self.convert_row_tid(tid_key="tid", key="name_en", rows=rows)

        json_path = os.path.join(self.config.json.base, self.config.json.predefined_decks)
        self.save_json(rows, json_path)
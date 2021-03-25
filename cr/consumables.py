"""
Generate rarities JSON from APK CSV source.
"""

import os

from csv2json import read_csv
from .base import BaseGen


class Consumables(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="consumables")

    def parse_tids(self, rows):
        for row in rows:
            row.update({
                '_lang': {
                    'name': self.text_all_lang(row['tid']),
                    'usage': self.text_all_lang(row['usage_tid']),
                    'usage_short': self.text_all_lang(row['usage_short_tid']),
                    'not_available': self.text_all_lang(row['not_available_tid']),
                    'invalid_target': self.text_all_lang(row['invalid_target_tid']),
                }
            })
        return rows

    def run(self):
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.consumables)
        rows = read_csv(csv_path)
        rows = self.value_dict_to_list(rows)
        rows = self.parse_tids(rows)

        json_path = os.path.join(self.config.json.base, self.config.json.consumables)
        self.save_json(rows, json_path)

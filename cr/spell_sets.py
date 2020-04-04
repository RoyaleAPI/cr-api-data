"""
Generate rarities JSON from APK CSV source.
"""

import os

from csv2json import read_csv
from .base import BaseGen


class SpellSets(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="spell_sets")

    def run(self):
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.spell_sets)
        rows = read_csv(csv_path)
        rows = self.value_dict_to_list(rows)

        # convert spells to keys
        for row in rows:
            spells = row.get('spells')
            card_keys = []
            for spell in spells:
                card = self.get_card(sc_key=spell)
                if not card:
                    card_keys.append(spell)
                else:
                    card_keys.append(card.get('key'))
            row['spells'] = card_keys



        json_path = os.path.join(self.config.json.base, self.config.json.spell_sets)
        self.save_json(rows, json_path)

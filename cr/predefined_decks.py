"""
Generate predefined decks JSON from APK CSV source.
"""

import os

from csv2json import read_csv
from .base import BaseGen



class PredefinedDecks(BaseGen):
    def __init__(self, config):
        super().__init__(config)
        self.i18n = True

    def run(self):
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.predefined_decks)
        rows = read_csv(csv_path)
        rows = self.value_dict_to_list(rows)
        rows = self.convert_row_tid(tid_key="tid", key="name_en", rows=rows)

        # convert sc_key in spells to keys
        for row in rows:
            spells = row.get('spells')
            if spells:
                cards = []
                for s in spells:
                    card = self.get_card(sc_key=s)
                    if card is not None:
                        cards.append(card.get('key'))
                row['spells'] = cards

            if self.i18n:
                tid = row.get('tid')
                if tid:
                    row.update({
                        '_lang': {
                            'name': self.text_all_lang(tid),
                        }
                    })

        json_path = os.path.join(self.config.json.base, self.config.json.predefined_decks)
        self.save_json(rows, json_path)
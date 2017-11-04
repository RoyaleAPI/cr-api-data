"""
Generate cards JSON from APK CSV source.
"""

import csv
import json
import os
import re

from .util import camelcase_split
from .base import BaseGen


class Cards(BaseGen):
    def __init__(self, config):
        super().__init__(config)

    def text(self, tid, lang):
        """Return field by TID and Language

        quests_hint = self.text('TID_HINT_QUESTS', 'EN')
        """
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.texts)
        with open(csv_path) as f:
            texts_reader = csv.DictReader(f)
            for row in texts_reader:
                if row[' '] == tid:
                    s = row[lang]
                    return s.replace('\q', '\"')
        return None

    def arena_id(self, key):
        """Return arena integer id by arena key."""
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.arenas)
        with open(csv_path) as f:
            texts_reader = csv.DictReader(f)
            for row in texts_reader:
                if row['Name'] == key:
                    return int(row['Arena'])
        return None

    def run(self):
        """Generate all jsons"""
        self.make_cards()

    def make_cards(self):
        """Generate cards.json"""

        cards = {}
        card_num = 0

        def card_type(card_config, card_num):
            """make card dicts by type."""
            csv_path = os.path.join(self.config.csv.base, card_config.csv)

            with open(csv_path, encoding="utf8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i > 0:
                        card_num += 1
                        if not row['NotInUse']:
                            card_id = card_num
                            name_en = self.text(row['TID'], 'EN')
                            name_strip = re.sub('[\.\-]', '', name_en)
                            ccs = camelcase_split(name_strip)
                            key = '-'.join(s.lower() for s in ccs)
                            card_key = '_'.join(s.lower() for s in ccs)
                            decklink = card_config.sckey.format(i - 1)
                            card = {
                                'card_id': card_id,
                                'key': key,
                                'card_key': card_key,
                                'name': name_en,
                                'elixir': int(row['ManaCost']),
                                'type': card_config.type,
                                'rarity': row['Rarity'],
                                'arena': self.arena_id(row['UnlockArena']),
                                'description': self.text(row['TID_INFO'], 'EN'),
                                'decklink': decklink
                            }

                            cards[card_id] = card
            return card_num

        for card_config in self.config.cards:
            card_num = card_type(card_config, card_num)

        json_path = os.path.join(self.config.json.base, self.config.json.cards)
        with open(json_path, 'w') as f:
            json.dump(cards, f, indent=4)

        print(json_path)



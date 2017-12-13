#!/usr/bin/env python
"""
Generate quests JSON from APK CSV source.
"""

import csv
import json
import os
import re

import yaml
from box import Box


def camelcase_split(s):
    """Split camel case into list of strings"""
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', s)


class App:
    def __init__(self, config_path=None):
        with open(config_path) as f:
            self.config = Box(yaml.load(f))

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
        """Return arena integer id by arena key
        """
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.arenas)
        with open(csv_path, encoding="utf8") as f:
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

        cards = []

        def card_type(type):
            """make card dicts by type."""
            spells = {
                'buildings': {
                    'path': self.config.csv.path.spells_buildings,
                    'type': 'Buildings',
                    'sckey': '270000{0:02d}'
                },
                'characters': {
                    'path': self.config.csv.path.spells_characters,
                    'type': 'Troops',
                    'sckey': '260000{0:02d}'
                },
                'other': {
                    'path': self.config.csv.path.spells_other,
                    'type': 'Spells',
                    'sckey': '280000{0:02d}'
                },
            }

            csv_path = os.path.join(self.config.csv.base, spells[type]['path'])
            with open(csv_path) as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i > 0 and 'NOTINUSE' not in row['Name']:
                        name = self.text(row['TID'], 'EN')
                        name_strip = name.replace('.', '')
                        ccs = camelcase_split(name_strip)
                        key = '-'.join(s.lower() for s in ccs)
                        decklink = spells[type]['sckey'].format(i - 1)
                        card = {
                            'key': key,
                            'name': name,
                            'elixir': int(row['ManaCost']),
                            'type': spells[type]['type'],
                            'rarity': row['Rarity'],
                            'arena': self.arena_id(row['UnlockArena']),
                            'description': self.text(row['TID_INFO'], 'EN'),
                            'decklink': decklink
                        }

                        cards.append(card)

        card_type('buildings')
        card_type('characters')
        card_type('other')

        json_path = os.path.join(self.config.json.base, self.config.json.cards)
        with open(json_path, 'w') as f:
            json.dump(cards, f, indent=4)


def test():
    pass


if __name__ == '__main__':
    app = App(config_path='./config.yml')
    app.run()

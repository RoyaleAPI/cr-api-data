#!/usr/bin/env python
"""
Generate cards JSON from APK CSV source.
"""

import csv
import os
import re
import json

import yaml
from box import Box


def camelcase_split(s):
    """Split camel case into list of strings"""
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', s)


class App:
    def __init__(self, config_path=None):
        with open(config_path) as f:
            self.config = Box(yaml.load(f))

        self.cards = {}

    def texts(self, tid, lang):
        """Return field by TID and Language

        quests_hint = self.texts('TID_HINT_QUESTS', 'EN')
        """
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.texts)
        with open(csv_path) as f:
            texts_reader = csv.DictReader(f)
            for row in texts_reader:
                if row[' '] == tid:
                    return row[lang]
        return None

    def run(self):
        """Generate all jsons"""
        self.make_cards()

    def make_cards(self):
        """Generate cards.json"""

        cards = []

        def card_type(type):
            """make card dicts by type."""
            if type == 'buildings':
                path = self.config.csv.path.spells_buildings
            elif type == 'characters':
                path = self.config.csv.path.spells_characters
            elif type == 'other':
                path = self.config.csv.path.spells_other

            csv_path = os.path.join(self.config.csv.base, path)
            with open(csv_path) as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i > 0:
                        card = {
                            'name': row['Name'],
                            'elixir': row['ManaCost'],
                            'type': type,
                            'rarity': row['Rarity'],
                            'arena': row['UnlockArena'],
                            'description': self.texts(row['TID_INFO'], 'EN')
                        }
                        cards.append(card)
                    else:
                        print(row.keys())

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

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

        cards = []

        def card_type(card_config):
            """make card dicts by type."""
            csv_path = os.path.join(self.config.csv.base, card_config.csv)

            with open(csv_path) as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i > 0:
                        if not row['NotInUse']:
                            name = self.text(row['TID'], 'EN')
                            name_strip = re.sub('[\.\-]', '', name)
                            ccs = camelcase_split(name_strip)
                            key = '-'.join(s.lower() for s in ccs)
                            decklink = card_config.sckey.format(i - 1)
                            card = {
                                'key': key,
                                'name': name,
                                'elixir': int(row['ManaCost']),
                                'type': card_config.type,
                                'rarity': row['Rarity'],
                                'arena': self.arena_id(row['UnlockArena']),
                                'description': self.text(row['TID_INFO'], 'EN'),
                                'decklink': decklink
                            }

                            cards.append(card)

        for card_config in self.config.cards:
            card_type(card_config)


        json_path = os.path.join(self.config.json.base, self.config.json.cards)
        with open(json_path, 'w') as f:
            json.dump(cards, f, indent=4)


def test():
    pass


if __name__ == '__main__':
    app = App(config_path='./config.yml')
    app.run()

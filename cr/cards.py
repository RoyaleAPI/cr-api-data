"""
Generate cards JSON from APK CSV source.
"""

import csv
import logging
import os
import re

from .base import BaseGen
from .util import camelcase_split

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Cards(BaseGen):
    def __init__(self, config):
        super().__init__(config)

    def arena_id(self, key):
        """Return arena integer id by arena key."""
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.arenas)
        with open(csv_path) as f:
            texts_reader = csv.DictReader(f)
            for row in texts_reader:
                if row['Name'] == key:
                    arena = row.get('Arena', 0)
                    if arena:
                        return int(arena)
                    else:
                        return 0
        return None

    def run(self):
        """Generate all jsons"""
        self.make_cards()

    def make_cards(self):
        """Generate cards.json"""

        cards = []
        card_num = 0

        card_keys = []

        def card_type(card_config, card_num):
            """make card dicts by type."""
            csv_path = os.path.join(self.config.csv.base, card_config.csv)

            with open(csv_path, encoding="utf8") as f:
                reader = csv.DictReader(f)
                # fix prince breaking things
                decklink_id_delta = 0
                for i, row in enumerate(reader):
                    if i > 0:
                        card_num += 1

                        process = True
                        if row['NotInUse']:
                            process = False
                        elif row['Name'].lower().startswith('notinuse'):
                            process = False
                        elif not row.get('Name'):
                            # Wizard / Prince oddity
                            process = False
                            decklink_id_delta -= 1

                        print(process, card_num, row)

                        if process:
                            tid = row.get('TID')
                            txt = self.text(tid, "EN")
                            print(txt)

                            name_en = self.text(row['TID'], 'EN')
                            if name_en == '':
                                name_en = row['Name']

                            if name_en is not None:
                                name_strip = re.sub('[.\-]', '', name_en)
                                ccs = camelcase_split(name_strip)
                                key = '-'.join(s.lower() for s in ccs)
                                # card_key = '_'.join(s.lower() for s in ccs)
                                decklink = card_config.sckey.format(i + decklink_id_delta - 1)
                                elixir = row.get('ManaCost')
                                if elixir:
                                    try:
                                        elixir = int(elixir)
                                    except Exception as e:
                                        print(e)
                                        elixir = 0
                                else:
                                    elixir = None

                                card = {
                                    'key': key,
                                    'name': name_en,
                                    'sc_key': row['Name'],
                                    'elixir': elixir,
                                    'type': card_config.type,
                                    'rarity': row['Rarity'],
                                    'arena': self.arena_id(row['UnlockArena']),
                                    'description': self.text(row['TID_INFO'], 'EN'),
                                    'id': int(decklink)
                                }

                                # skip unreleased cards
                                if key in ['wolf-rider', 'prison-goblin']:
                                    continue

                                # ensure unique keys — dev builds have non unique keys
                                if key not in card_keys:
                                    card_keys.append(key)
                                    cards.append(card)
                                    logger.info(card)
                                else:
                                    logger.warning(f"Duplicate card key: {key}, skipping…")
            return card_num

        for card_config in self.config.cards:
            card_num = card_type(card_config, card_num)

        json_path = os.path.join(self.config.json.base, self.config.json.cards)

        self.save_json(cards, json_path)

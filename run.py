#!/usr/bin/env python
"""
Generate data JSON from APK CSV source.
"""

import yaml
from box import Box
import sys

from cr import *

sys.path.append('./lib/cr-csv-parser')

if __name__ == '__main__':
    config_path = './config.yml'

    with open(config_path) as f:
        config = Box(yaml.safe_load(f))

    to_run = []

    # v2 runs
    to_run.extend([
        TextsGen,
        BattleTimelines,
        Arenas,
        Rarities,
        PredefinedDecks,
        AllianceBadges,
        GameModes,
        Challenges,
        SpellSets,
        DraftDeck,
    ])

    # legacy to be converted
    to_run.extend([
        Cards,
        ChestOrder,
        ClanChest,
        Regions,
        TreasureChests,
        CardStats,
        Tournaments,
    ])

    # i18n
    i18_to_run = [
        Cards,
    ]

    for cls in to_run:
        app = cls(config=config)
        app.run()

    for cls in i18_to_run:
        app = cls(config=config, i18n=True)
        app.run()

#!/usr/bin/env python
"""
Generate data JSON from APK CSV source.
"""

import yaml
from box import Box

from cr import *

if __name__ == '__main__':
    config_path = './config.yml'

    with open(config_path) as f:
        config = Box(yaml.safe_load(f))

    to_run = [
        # AllianceBadges,
        # Cards,
        # Rarities,
        # ChestOrder,
        # ClanChest,
        # GameModes,
        # Regions,
        Arenas,
        # TreasureChests,
        # CardStats,
        # Tournaments,
        # Challenges
    ]

    for cls in to_run:
        app = cls(config=config)
        app.run()

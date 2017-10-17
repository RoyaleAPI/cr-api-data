#!/usr/bin/env python
"""
Generate data JSON from APK CSV source.
"""

from cr.cards import Cards
from cr.rarities import Rarities
from cr.chests import Chests
from box import Box
import yaml

if __name__ == '__main__':
    config_path = './config.yml'

    with open(config_path) as f:
        config = Box(yaml.load(f))

    app = Cards(config=config)
    app.run()

    app = Rarities(config=config)
    app.run()

    app = Chests(config=config)
    app.run()


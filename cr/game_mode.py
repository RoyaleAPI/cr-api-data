"""
Game modes
"""

import csv
import os

from .base import BaseGen
from .util import camelcase_split


class GameModes(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="game_modes", null_int=True)

        self.exclude_fields = [
            "RequestTID",
            "InProgressTID",
            "Icon",
            "EndConfetti1",
            "EndConfetti2"
        ]

    def run(self):
        data = self.load_csv(exclude_empty=True)
        out = []
        for i, row in enumerate(data):
            id_ = i + 2 - 9
            if id_ > 0:
                row.update({
                    'id': int(self.config.scid.game_modes.format(id_)),
                })
                out.append(row)

        out = [o for o in out if o['id']]
        self.save_json(out)






"""
Generate arenas JSON from APK CSV source.
"""

import csv
import os

from .base import BaseGen
from .util import camelcase_split


class AllianceBadges(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="alliance_badges", null_int=True)

    def run(self):
        data = self.load_csv(exclude_empty=True)
        for id, row in enumerate(data):
            row['badge_id'] = 16000000 + id
        self.save_json(data)






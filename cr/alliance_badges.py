"""
Clan badges
"""

from .base import BaseGen
from csv2json import read_csv


class AllianceBadges(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="alliance_badges", null_int=True)

    def run(self):
        data = read_csv(self.csv_path)

        # data = self.load_csv(exclude_empty=True)
        for id, row in enumerate(data):
            row['id'] = 16000000 + id
        self.save_json(data)

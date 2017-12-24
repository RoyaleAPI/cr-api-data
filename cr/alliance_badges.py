"""
Clan badges
"""

from .base import BaseGen


class AllianceBadges(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="alliance_badges", null_int=True)

    def run(self):
        data = self.load_csv(exclude_empty=True)
        for id, row in enumerate(data):
            row['id'] = 16000000 + id
        self.save_json(data)

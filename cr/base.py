"""
Base generator
"""

import csv
import os


class BaseGen:
    def __init__(self, config):
        self.config = config

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

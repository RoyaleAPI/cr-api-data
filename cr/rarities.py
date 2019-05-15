"""
Generate rarities JSON from APK CSV source.
"""

import csv
import json
import os

from .base import BaseGen
from .util import camelcase_split

from csv2json import read_csv


class Rarities(BaseGen):
    def __init__(self, config):
        super().__init__(config)

    def run(self):
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.rarities)
        rows = read_csv(csv_path)
        rows = self.value_dict_to_list(rows)

        json_path = os.path.join(self.config.json.base, self.config.json.rarities)
        self.save_json(rows, json_path)





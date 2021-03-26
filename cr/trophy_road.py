"""
Generate rarities JSON from APK CSV source.
"""

import os

from csv2json import read_csv
from .base import BaseGen
import csv

from .util import camelcase_to_snakecase


class TrophyRoad(BaseGen):
    """
    Trophy road should be road as strict dicts
    """
    def __init__(self, config):
        super().__init__(config, id="trophy_road")

    def run(self):
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.trophy_road)

        rows = []

        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = {camelcase_to_snakecase(k): v for k, v in row.items()}
                rows.append(item)

        # first row is value type
        value_type = {k.lower(): v for k, v in rows[0].items()}
        items = []

        print(len(rows))
        for row in rows[1:]:
            for k, v in row.items():
                v_type = value_type.get(k)
                if not v:
                    row[k] = None
                elif v_type == 'int':
                    row[k] = int(v)

            items.append(row)

        print(len(items))


        json_path = os.path.join(self.config.json.base, self.config.json.trophy_road)
        self.save_json(items, json_path)

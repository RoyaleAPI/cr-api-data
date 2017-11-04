"""
Generate regions
"""
import csv
import os

from .base import BaseGen


class Regions(BaseGen):
    def __init__(self, config):
        super().__init__(config)

    def run(self):
        """Generate regions jsons"""
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.regions)

        regions = []

        with open(csv_path, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i > 0:
                    regions.append({
                        'id': 57000000 + i - 1,
                        'key': row.get('Name'),
                        'name': row.get('DisplayName'),
                        'isCountry': row.get('IsCountry') == 'TRUE'
                    })

        json_path = os.path.join(self.config.json.base, self.config.json.regions)
        self.save_json(regions, json_path)

"""
Challenges
"""

from csv2json import read_csv
from .base import BaseGen


class Challenges(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="challenges", null_int=False)

    def run(self):
        data = read_csv(self.csv_path)

        for i, row in enumerate(data):
            row_name = row.get('name')
            if row_name is None:
                continue
            row.update(dict(
                key=row_name,
                id=65000000 + i,
            ))
            if row.get('tid'):
                row.update(dict(
                    name_en=self.text(row["tid"], "EN")
                ))

        data = self.value_dict_to_list(data)

        self.save_json(data)

"""
Game modes
"""

from csv2json import read_csv
from .base import BaseGen


class Emotes(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="emotes", null_int=True)

    def run(self):
        data_list = read_csv(self.csv_path)

        out = []
        for index, row in enumerate(data_list):
            if row.get('name') is not None:
                # print(row.get('name'))
                hi = row.get('index_hi', '')
                lo = row.get('index_lo', '')
                sc = row.get('sc_file', '')[3:] # truncate path sc/
                row.update(
                    key=f"emote_{hi}_{lo}",
                    file_key=f"{sc}:{hi}:{lo}"
                )
                out.append(row)

        self.save_json(out)

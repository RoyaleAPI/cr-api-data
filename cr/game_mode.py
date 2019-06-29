"""
Game modes
"""

from csv2json import read_csv
from .base import BaseGen


class GameModes(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="game_modes", null_int=True)

    def run(self):
        data_list = read_csv(self.csv_path)

        out = []
        id_ = 0
        for index, row in enumerate(data_list):
            if row.get('name') is not None:
                row.update({
                    'id': int(self.config.scid.game_modes.format(id_)),
                    'name_en': row.get('name_en') or row.get('name'),
                })

                id_ += 1

                row = self.row_parse_tid(row)
                row = self.row_parse_dict_list(row)
                row = self.row_force_list(row, "predefined_decks")

                out.append(row)

        out = [o for o in out if o['id']]
        self.save_json(out)

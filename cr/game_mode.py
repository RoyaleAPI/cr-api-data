"""
Game modes
"""

from .base import BaseGen
import os

from csv2json import read_csv


class GameModes(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="game_modes", null_int=True)

        # self.exclude_fields = [
        #     "RequestTID",
        #     "InProgressTID",
        #     "Icon",
        #     "EndConfetti1",
        #     "EndConfetti2",
        #     "ForcedDeckCardsUsingCardTheme",
        #     "PrincessSkin",
        #     "KingSkin"
        # ]

    def run(self):
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.game_modes)
        data_list = read_csv(csv_path)

        out = []
        id_ = 0
        for index, row in enumerate(data_list):
            if row.get('name') is not None:
                row.update({
                    'id': int(self.config.scid.game_modes.format(id_)),
                    'name_en':  row.get('name_en') or row.get('name'),
                })

                id_ += 1

                row = self.row_parse_tid(row)
                row = self.row_parse_dict_list(row)

                out.append(row)

        out = [o for o in out if o['id']]
        self.save_json(out)


        # data = self.load_csv(
        #     exclude_empty=True,
        #     tid_fields=[
        #         {"field": "ClanWarDescription", "output_field": "clan_war_description"}
        #     ]
        # )
        # out = []
        # id_ = 0
        # for i, row in enumerate(data):
        #     if row.get('name') is not None:
        #         row.update({
        #             'id': int(self.config.scid.game_modes.format(id_)),
        #             'name_en':  row.get('name_en') or row.get('name'),
        #         })
        #         out.append(row)
        #         id_ += 1
        #
        # out = [o for o in out if o['id']]
        # self.save_json(out)

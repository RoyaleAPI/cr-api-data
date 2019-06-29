"""
Generate arenas JSON from APK CSV source.
"""

from csv2json import read_csv
from .base import BaseGen


class Arenas(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="arenas", null_int=True)

    def arena_key(self, row):
        """unique key of the arena. Used for image assets."""
        if int(row["arena"]) <= 12:
            return "arena{}".format(row["arena"])
        else:
            return "league{}".format(row["name"][-1])

    def run(self):
        """Generate json."""
        arenas = read_csv(self.csv_path)

        # add scid
        base_scid = 54000000
        for index, row in enumerate(arenas):
            arena_id = min(12, row["arena"])
            league_id = max(0, row['arena'] - 12)
            row.update({
                "id": base_scid + index,
                "key": self.arena_key(row),
                "title": self.text(row["tid"], "EN"),
                "subtitle": self.text(row["subtitle_tid"], "EN"),
                "arena_id": arena_id,
                "league_id": league_id,
            })
            row.pop('tid', None)
            row.pop('subtitle_tid', None)

        # sort arenas by trophy limit
        arenas = sorted(arenas, key=lambda x: x['trophy_limit'])

        self.save_json(arenas)

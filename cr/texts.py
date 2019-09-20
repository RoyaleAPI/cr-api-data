"""
Text: i18n full
"""

from csv2json import read_csv
from .base import BaseGen


class TextsGen(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="texts", json_id="texts", null_int=True)

    def convert_text(self, csv_path, first_key=None):
        data_list = read_csv(csv_path)

        out = []
        for index, row in enumerate(data_list):
            row["sc_key"] = row.pop(first_key)

            # replace quotes
            for k, v in row.items():
                if "\\q" in v:
                    s = v
                    toggle = 0
                    while "\\q" in s:
                        if toggle == 0:
                            s = s.replace('\\q', '“', 1)
                        else:
                            s = s.replace('\\q', '”', 1)
                        toggle += 1
                    row[k] = s

            out.append(row)

        return out

    def run(self):
        out = []
        out.extend(
            self.convert_text(
                self.csv_path,
                first_key="e"
             )
        )
        out.extend(
            self.convert_text(
                self.csv_path_by_id(id="texts_patch"),
                first_key=" "
            )
        )

        # convert list to dict
        ret = dict()
        for o in out:
            ret[o.get('sc_key')] = o

        self.save_json(ret)

"""
Base generator
"""

import csv
import json
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

    def row_value(self, row, field, types):
        """Row value cast with field type.

        SC’s CSVs uses the second row as type in the CSV.
        """
        value = row.get(field)
        if types[field] == 'boolean':
            return row[field] == 'TRUE'
        elif value == '':
            return None
        elif types[field] == 'string':
            return str(row[field])
        elif types[field] == 'Int':
            return int(row[field])
        else:
            return row[field]

    def save_json(self, data, json_path):
        """Save path to json."""
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(json_path)

    def run(self):
        """Abstract method."""
        pass

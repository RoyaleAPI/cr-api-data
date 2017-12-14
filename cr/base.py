"""
Base generator
"""

import csv
import json
import os


class BaseGen:
    def __init__(self, config, id=None):
        self.config = config

        self.csv_path = None
        self.json_path = None
        if id is not None:
            self.csv_path = self.csv_path_by_id(id)
            self.json_path = self.json_path_by_id(id)

        self._field_types = None
        self._arenas = None

    def csv_path_by_id(self, id):
        return os.path.join(self.config.csv.base, self.config.csv.path[id])

    def json_path_by_id(self, id):
        return os.path.join(self.config.json.base, self.config.json[id])

    @property
    def field_types(self):
        """Dict of type by field name"""
        if self._field_types is None:
            with open(self.csv_path, encoding="utf8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i == 0:
                        self._field_types = {k: v for k, v in row.items()}
        return self._field_types

    @property
    def arenas(self):
        """Arenas dict from json."""
        if self._arenas is None:
            self._arenas = self.load_json(self.json_path_by_id("arenas"))
        return self._arenas

    def get_arena(self, name):
        """Return arena dict by name."""
        for arena in self.arenas:
            if arena["name"] == name:
                return arena
        return None

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

    def row_value(self, row, field):
        """Row value cast with field type.

        SC’s CSVs uses the second row as type in the CSV.
        """
        value = row.get(field)
        if field not in self.field_types:
            return None
        elif self.field_types[field].lower() == 'boolean':
            return value == 'TRUE'
        elif self.field_types[field].lower() == 'int':
            if value == '':
                return 0
            return int(value)
        elif value == '':
            return None
        elif self.field_types[field].lower() == 'string':
            return str(value)
        else:
            return value

    def load_json(self, json_path):
        """Load json from path."""
        with open(json_path, encoding='utf-8', mode='r') as f:
            data = json.load(f)
        return data

    def save_json(self, data, json_path):
        """Save path to json."""
        with open(json_path, encoding='utf-8', mode='w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(json_path)

    def run(self):
        """Abstract method."""
        pass

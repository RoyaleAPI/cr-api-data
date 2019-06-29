"""
Base generator
"""

import csv
import json
import os

from .util import camelcase_to_snakecase


class TextField:
    def __init__(self, input, output):
        self.input = input
        self.output = output


class BaseGen:
    """Base generator.

    Args:
        config: config.yaml
        id: csv / json id, e.g. arenas
        null_int: if null value for int fields should be null of 0. Default: False, i.e. 0
    """

    def __init__(self, config, id=None, json_id=None, null_int=False):
        self.config = config

        self._id = id
        self._json_id = json_id

        self.include_fields = []
        self.exclude_fields = []
        self.tid_fields = []
        self._field_types = None
        self._arenas = None

        self.null_int = null_int

    @property
    def csv_path(self):
        p = None
        if self._id is not None:
            p = self.csv_path_by_id(self._id)
        return p

    @property
    def json_path(self):
        p = None
        if self._json_id is not None:
            p = self.json_path_by_id(self._json_id)
        elif self._id is not None:
            p = self.json_path_by_id(self._id)
        return p

    def csv_path_by_id(self, id):
        return os.path.join(self.config.csv.base, self.config.csv.path[id])

    def json_path_by_id(self, id):
        if id in self.config.json:
            return os.path.join(self.config.json.base, self.config.json[id])
        return None

    def value_dict_to_list(self, rows):
        """Convert values in dict rows to lists"""
        for row in rows:
            for k, v in row.items():
                if isinstance(v, dict):
                    if any([str(vk).isdigit() for vk, vv in v.items()]):
                        row[k] = list(v.values())
        return rows

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

    def text(self, tid, lang="EN"):
        """Return field by TID and Language

        quests_hint = self.text('TID_HINT_QUESTS', 'EN')
        """
        csv_paths = [
            os.path.join(self.config.csv.base, self.config.csv.path.texts),
            os.path.join(self.config.csv.base, self.config.csv.path.texts_patch)
        ]
        _text = None
        while _text is None:
            for csv_path in csv_paths:
                with open(csv_path, encoding="utf8") as f:
                    texts_reader = csv.DictReader(f)
                    for row in texts_reader:
                        keys = ['v', 'e', ' ']
                        for key in keys:
                            if key in row.keys():
                                if row.get(key) == tid:
                                    s = row[lang]
                                    _text = s.replace('\q', '\"')
            if _text is None:
                _text = ''

        return _text

    def convert_row_tid(self, tid_key=None, key=None, rows=None, lang="EN", remove_tid_key=False):
        rows = rows or []

        for row in rows:
            if tid_key in row.keys():
                tid = row.get(tid_key)
                if tid is not None:
                    txt = self.text(tid, lang=lang)
                    row[key] = txt
                    if remove_tid_key:
                        row.pop(tid_key)

        return rows

    def row_value(self, row, field):
        """Row value cast with field type.

        SC’s CSVs uses the second row as type in the CSV.
        """
        value = row.get(field)
        if field not in self.field_types:
            return None

        field_type = self.field_types.get(field)
        if not field_type:
            return None

        if field_type.lower() == 'boolean':
            if not value:
                return False
            return value.lower() == 'true'

        if field_type.lower() == 'int':
            if not value:
                if self.null_int:
                    return None
                else:
                    return 0
            return int(value)
        elif value == '':
            return None
        elif self.field_types[field].lower() == 'string':
            return str(value)
        else:
            return value

    def load_csv(self, exclude_empty=False, tid_fields=None, inherit_previous=False):
        """Load CSV into dict.

        Params:
            exclude_empty:     ignore empty fields
            tid_fields:        list of fields to convert using the TID csv
                               [{"field": "TID", "output_field": "name_en"}]
            inherit_previous:  copy the previou row’s value if field is empty.
        """
        if tid_fields is None:
            tid_fields = [{"field": "TID", "output_field": "name_en"}]
        if self.csv_path is None:
            return None
        items = []
        with open(self.csv_path, encoding="utf8")  as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i > 0:

                    item = {}
                    for k, v in row.items():
                        if exclude_empty and row[k] == '' and self.field_types.get(k).lower() != 'boolean':
                            continue

                        # Include all fields unless it is set
                        if len(self.include_fields) and k not in self.include_fields:
                            continue

                        # Don’t include if in exclude fields
                        if k in self.exclude_fields:
                            continue

                        # Exclude fields with _effects int it
                        if k.endswith('Effect'):
                            continue

                        # Exclude shadows
                        if k.startswith('Shadow'):
                            continue

                        if k.lower().endswith('exportname'):
                            continue

                        # Exclude known non-stat fileds
                        if k.lower() in [
                            "filename", "useanimator", "iconswf", "tid"]:
                            continue

                        # camelcase split, keep digits at end

                        item[camelcase_to_snakecase(k)] = self.row_value(row, k)

                    # text fields
                    for tf in tid_fields:
                        if row.get(tf["field"]):
                            item[tf["output_field"]] = self.text(row[tf["field"]], "EN")

                    items.append(item)

        return items

    def load_json(self, json_path=None):
        """Load json from path."""
        if json_path is None:
            json_path = self.json_path
        with open(json_path, encoding='utf-8', mode='r') as f:
            data = json.load(f)
        return data

    def save_json(self, data, json_path=None):
        """Save path to json."""
        if json_path is None:
            json_path = self.json_path
        with open(json_path, encoding='utf-8', mode='w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(json_path)

    def run(self):
        """Abstract method."""
        pass

    def row_parse_tid(self, row):
        """Convert TID values into text."""
        for k, v in row.items():
            if isinstance(v, str) and v.startswith('TID'):
                row[k] = self.text(tid=v, lang="EN")
        tid = row.get('tid')
        if tid:
            row['name_en'] = tid

        return row

    def row_parse_dict_list(self, row):
        """Convert dict lists as simple lists."""
        for k, v in row.items():
            if isinstance(v, dict):
                row[k] = list(v.values())
        return row

    def row_force_list(self, row, key):
        """Force a key to always output lists."""
        for k, v in row.items():
            if k != key:
                continue

            if isinstance(v, str):
                row[k] = [v]

        return row

    def get_card(self, sc_key=None):
        """Convert SC card keys to keys"""
        with open(self.json_path_by_id(id="cards")) as f:
            cards = json.load(f)

        if sc_key is not None:
            for c in cards:
                if c.get('sc_key') == sc_key:
                    return c

        return None

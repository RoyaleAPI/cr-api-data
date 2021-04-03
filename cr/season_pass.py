"""
Generate rarities JSON from APK CSV source.
"""

import csv
import os
from typing import List

from pydantic import BaseModel

from .base import BaseGen
from .util import camelcase_to_snakecase
from collections import defaultdict


class SeasonPassItem(BaseModel):
    name: str
    summary: dict = {}
    rows: List[dict] = []

    def summarize(self):
        """
        Go through the list and count items
        :return:
        """
        s_dict = defaultdict(int)
        for row in self.rows:
            s_key = None
            amount = 0
            if row.get('token'):
                s_key = f"token_{row.get('token')}"
            elif row.get('consumable'):
                s_key = f"consumable_{row.get('consumable')}"
            elif row.get('resource'):
                s_key = f"resource_{row.get('resource')}"

            if s_key is not None:
                amount = row.get('amount')

                s_dict[s_key] += amount

        self.summary = s_dict







class SeasonPassPro(BaseGen):
    """
    Trophy road should be road as strict dicts
    """
    config_id = 'season_pass_pro'

    def __init__(self, config):
        super().__init__(config, id=self.config_id)

    def create_summary(self, rows):
        """
        Create a summary based on
        :param rows:
        :return:
        """

    def run(self):
        csv_path = os.path.join(
            self.config.csv.base,
            getattr(self.config.csv.path, self.config_id)
        )

        rows = []

        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = {camelcase_to_snakecase(k): v for k, v in row.items()}
                rows.append(item)

        # first row is value type
        value_type = {k.lower(): v for k, v in rows[0].items()}
        items = dict()

        current_name = None
        current_name_count = 0
        item_rows = []
        is_new_item = False
        current_item = None

        for row in rows[1:]:

            for k, v in row.items():
                v_type = value_type.get(k)
                if not v:
                    row[k] = None
                elif v_type == 'int':
                    row[k] = int(v)
                elif v_type == 'boolean':
                    if v.lower() == 'true':
                        row[k] = True
                    else:
                        row[k] = False

            # parse name
            name = row.get('name')
            crowns = row.get("crowns") or 0
            premium = 1 if row.get('premium') else 0
            if name:
                current_name = name
                is_new_item = True
            else:
                is_new_item = False

            row_name = f"{current_name}_{crowns:04d}_{premium}"
            # print(row_name)
            row['name'] = row_name

            if is_new_item:
                current_item = SeasonPassItem(
                    name=current_name,
                    rows=[row],
                    summary=dict(),
                )
            else:
                current_item.rows.append(row)

            # print(current_item)

            items[current_item.name] = current_item

            # items.append(row)

        for k, item in items.items():
            item.summarize()

        json_path = os.path.join(
            self.config.json.base,
            getattr(self.config.json, self.config_id)
        )
        self.save_json(
            [v.dict() for k, v in items.items()],
            json_path
        )


class SeasonPassRookie(SeasonPassPro):
    config_id = 'season_pass_rookie'

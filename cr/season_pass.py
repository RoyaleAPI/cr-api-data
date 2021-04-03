"""
Generate rarities JSON from APK CSV source.
"""

import csv
import os
from collections import defaultdict
from collections import OrderedDict
from typing import List

from pydantic import BaseModel

from .base import BaseGen
from .util import camelcase_to_snakecase


class SeasonPassItem(BaseModel):
    name: str
    summary: dict = {}
    summary_free: dict = {}
    summary_paid: dict = {}
    rows: List[dict] = []

    def summarize(self):
        """
        Go through the list and count items
        :return:
        """
        s_dict = defaultdict(int)
        s_free = defaultdict(int)
        s_paid = defaultdict(int)

        for row in self.rows:
            s_key = None
            amount = 0
            if row.get('token'):
                s_key = f"token_{row.get('token')}"
            elif row.get('consumable'):
                s_key = f"consumable_{row.get('consumable')}"
            elif row.get('resource'):
                s_key = f"resource_{row.get('resource')}"
            elif row.get('strike') is True:
                s_key = "strike"
            elif row.get('bonus_consumable'):
                s_key = f"bonus_consumable_{row.get('bonus_consumable')}"
            elif row.get('emote_id_high'):
                s_key = "emote"
            elif row.get('bonus_emote_id_high'):
                s_key = "bonus_emote"
            elif row.get('chest'):
                s_key = f"chest_{row.get('chest')}"

            if s_key is not None:
                if s_key.startswith('bonus'):
                    amount = row.get('bonus_consumable_amount')
                elif row.get('amount'):
                    amount = row.get('amount')
                else:
                    amount = 1


                try:
                    if amount is None:
                        amount = 1
                    s_dict[s_key] += amount

                    if row.get('premium') is True:
                        s_paid[s_key] += amount
                    else:
                        s_free[s_key] += amount
                except TypeError:
                    print(s_key, amount)
                    print(s_key == 'bonus_emote')
                    print(s_key in ['emote', 'bonus_emote'])
                    raise

        # add one strike to strikes, which is added upon unlock
        for sd in [s_dict, s_paid, s_free]:
            if 'strike' in sd.keys():
                sd['strike'] += 1

        # sort dict
        s_dict = OrderedDict(sorted(s_dict.items()))
        s_paid = OrderedDict(sorted(s_paid.items()))
        s_free = OrderedDict(sorted(s_free.items()))

        self.summary = s_dict
        self.summary_paid = s_paid
        self.summary_free = s_free

    def summary_dict(self):
        """
        Create a dict without rows
        :return:
        """
        return {k: v for k, v in self.dict().items() if k not in ['rows']}


class SeasonPassPro(BaseGen):
    """
    Trophy road should be road as strict dicts
    """
    config_id = 'season_pass_pro'
    config_summary_id = 'season_pass_pro_summary'

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

        self.save_json(
            [v.dict() for k, v in items.items()],
            os.path.join(
                self.config.json.base,
                getattr(self.config.json, self.config_id)
            )
        )
        self.save_json(
            [v.summary_dict() for k, v in items.items()],
            os.path.join(
                self.config.json.base,
                getattr(self.config.json, self.config_summary_id)
            )
        )


class SeasonPassRookie(SeasonPassPro):
    config_id = 'season_pass_rookie'
    config_summary_id = 'season_pass_rookie_summary'

"""
Challenges
"""

from .base import BaseGen

class Challenges(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="challenges", null_int=False)
        self.include_fields = [
            'Name',
            'GameMode', 'Enabled', 'JoinCost', 'JoinCostResource',
            'MaxWins', 'MaxLoss', 'RewardCards', 'RewardGold',
            'RewardSpell', 'RewardSpellMaxCount', 'TID'
        ]

    def run(self):
        data = self.load_csv()
        out = []
        item = None

        for i, row in enumerate(data):
            row_name = row.get('name')
            if row_name is not None:
                if item is not None:
                    out.append(item)
                item = row.copy()
                item['key'] = item['name']
            else:
                for field in ['reward_cards', 'reward_gold']:
                    if row.get(field):
                        if not isinstance(item.get(field), list):
                            item[field] = [item[field]]
                        item[field].append(row[field])

        # include last row
        out.append(item)

        # remove disabled
        # out = [o for o in out if o['enabled']]

        self.save_json(out)
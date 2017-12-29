"""
Tournaments
"""

from .base import BaseGen


class Tournaments(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="tournaments", null_int=True)

    def run(self):
        data = self.load_csv(exclude_empty=True)
        out = []
        for i, row in enumerate(data):
            if not row['disabled']:
                # convert name to key
                row['key'] = row['name']
                row.pop('name')

                # turn prizes into ordered dict
                prizes = [
                    {'rank': int(k[5:]), 'cards': v}
                    for i, (k, v) in enumerate(row.items())
                    if k.startswith('prize')]
                for i, prize in enumerate(prizes, 1):
                    prize['tier'] = i

                for k, v in row.copy().items():
                    if k.startswith('prize'):
                        row.pop(k)
                row['prizes'] = prizes

                # add card count as list
                cards = []
                for rank in range(row['max_players']):
                    rank_cards = 0
                    for prize in prizes:
                        if rank + 1 <= prize['rank']:
                            rank_cards = prize['cards']
                            break
                    cards.append(rank_cards)
                row['cards'] = cards

                # remove non-data fields
                row.pop('disabled')
                row.pop('version')



                out.append(row)

        self.save_json(out)
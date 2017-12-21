"""
Treasure chests generator
"""
import re

from .base import BaseGen


class TreasureChests(BaseGen):

    def __init__(self, config):
        super().__init__(config, id="treasure_chests")

        self.config = config

        self.include_fields = ["Name", "BaseChest", "Arena", "InShop", "InArenaInfo", "TournamentChest",
                               "SurvivalChest",
                               "ShopPriceWithoutSpeedUp", "TimeTakenDays", "TimeTakenHours", "TimeTakenMinutes",
                               "TimeTakenSeconds", "RandomSpells", "DifferentSpells", "ChestCountInChestCycle",
                               "RareChance",
                               "EpicChance", "LegendaryChance", "SkinChance", "GuaranteedSpells", "MinGoldPerCard",
                               "MaxGoldPerCard", "SpellSet", "Exp", "SortValue", "SpecialOffer", "DraftChest",
                               "BoostedChest",
                               "LegendaryOverrideChance"
                               ]
        self.tid_fields = [
            dict(field="TID", output_field="description"),
            dict(field="NotificationTID", output_field="notification")
        ]

        self.base_chests = []
        self.items = []

    def get_base_chest_stats(self, name):
        """Return base chest stats as dict."""
        props = [
            "time_taken_hours", "time_taken_minutes", "time_taken_seconds",
            "random_spells", "different_spells",
            "chest_count_in_chest_cycle",
            "rare_chance", "epic_chance", "legendary_chance", "skin_chance",
            "min_gold_per_card", "max_gold_per_card",
            "sort_value"
        ]
        for item in self.items:
            if name == item["name"]:
                return {k: v for k, v in item.items() if k in props}
        return {}

    def card_count_by_arena(self, name, random_spells, chest_reward_multiplier):
        # don’t scale legendary chests
        if name.startswith('Legendary'):
            return int(random_spells)
        # don’t scale epic chests
        if name.startswith('Epic'):
            return int(random_spells)
        # don’t scale draft chest rewards
        if name.startswith("Draft"):
            return int(random_spells)
        # don’t scale season rewards
        if name.startswith("SeasonReward"):
            return int(random_spells)

        if chest_reward_multiplier:
            return int(chest_reward_multiplier / 100 * random_spells)
        return 0

    def card_count_by_type(self, card_count_by_arena, chance):
        if chance == 0:
            return 0
        return 1 / chance * card_count_by_arena

    def include_item(self, item):
        """Return true if chest shoule be included."""
        name = item['name']
        if name is None:
            return False
        if len(name) == 0:
            return False
        # Exclude old chests
        if re.match('.+_old', name):
            return False
        # Exclude clan chest
        if name.startswith('ClanCrownChest'):
            return False
        # Exclude tournament chests
        if name.startswith('Tournament'):
            return False
        # Exclude challenge chests
        if name.startswith('Survival'):
            return False
        # Exclude rows with base
        if item['base_chest']:
            return False
        # Exclude if not in shop nor in cycle: e.g. arena 1 draft chest
        # if not item['in_shop'] and item['chest_count_in_chest_cycle'] == 0:
        #     return False
        return True

    def run(self):
        """Generate treasure chests."""
        data = self.load_csv(tid_fields=self.tid_fields)
        items = []

        # include relevant chests
        for d in data:
            if self.include_item(d):
                item = d.copy()

                # include arena info if relevant
                arena = item.get('arena')
                if arena:
                    arena_dict_keys = [
                        "name", "arena", "key", "chest_reward_multiplier", "shop_chest_reward_multiplier",
                        "title", "subtitle"
                    ]
                    arena_dict = self.get_arena(arena)
                    if arena_dict is not None:
                        arena_dict = {k: v for k, v in arena_dict.items() if k in arena_dict_keys}
                        item['arena'] = arena_dict

                # Card count = random spells
                item["card_count"] = item["random_spells"]

                # Gold output is affected by card count
                item["min_gold"] = item["card_count"] * item["min_gold_per_card"]
                item["max_gold"] = item["card_count"] * item["max_gold_per_card"]

                item["arenas"] = []

                items.append(item)

        # chests in shop
        shop_chests = [item for item in items if item['in_shop']]
        shop_chests = sorted(shop_chests, key=lambda x: x['sort_value'])

        # crown chests
        crown_chests = [item for item in items if item['name'].startswith('Star')]
        crown_chests = sorted(crown_chests, key=lambda x: x['sort_value'])

        # chests in cycle
        cycle_chests = [item for item in items if item['chest_count_in_chest_cycle']]
        cycle_chests = sorted(cycle_chests, key=lambda x: x['sort_value'])

        for chest in [c for c in cycle_chests if c['name'] != 'Legendary']:
            chest['arenas'] = []
            for arena in self.arenas:
                arena_dict = arena.copy()
                arena_dict_keys = [
                    "name", "arena", "key", "chest_reward_multiplier", "shop_chest_reward_multiplier",
                    "title", "subtitle"
                ]
                if arena_dict is not None:
                    arena = {k: v for k, v in arena_dict.items() if k in arena_dict_keys}

                    # arena affects these fields
                    card_count_by_arena = self.card_count_by_arena(
                        item["name"],
                        item["card_count"],
                        arena.get("chest_reward_multiplier")
                    )
                    card_count_rare = self.card_count_by_type(card_count_by_arena, item["rare_chance"])
                    card_count_epic = self.card_count_by_type(card_count_by_arena, item["epic_chance"])
                    card_count_legendary = self.card_count_by_type(card_count_by_arena,
                                                                   item["legendary_chance"])
                    card_count_common = card_count_by_arena - card_count_rare - card_count_epic - card_count_legendary

                    arena.update({
                        "card_count_by_arena": card_count_by_arena,
                        "card_count_common": card_count_common,
                        "card_count_rare": card_count_rare,
                        "card_count_epic": card_count_epic,
                        "card_count_legendary": card_count_legendary,
                    })

                    chest['arenas'].append(arena)




        # add arena cards to base chests
        # for item in items:
        #     if item['name'] in ['Free', 'Silver', 'Gold', 'Magic', 'Giant', 'Super', 'Star', 'StarBoosted']:
        #         for d in data:
        #             if d['base_chest'] == item['name']:
        #                 arena_dict = self.get_arena(d["arena"])
        #                 arena_dict_keys = [
        #                     "name", "arena", "key", "chest_reward_multiplier", "shop_chest_reward_multiplier",
        #                     "title", "subtitle"
        #                 ]
        #                 if arena_dict is not None:
        #                     arena = {k: v for k, v in arena_dict.items() if k in arena_dict_keys}
        #
        #                     # arena affects these fields
        #                     card_count_by_arena = self.card_count_by_arena(
        #                         item["name"],
        #                         item["card_count"],
        #                         arena.get("chest_reward_multiplier")
        #                     )
        #                     item["card_count_by_arena"] = card_count_by_arena
        #
        #                     # area affects total card chance
        #                     card_count_rare = self.card_count_by_type(card_count_by_arena, item["rare_chance"])
        #                     card_count_epic = self.card_count_by_type(card_count_by_arena, item["epic_chance"])
        #                     card_count_legendary = self.card_count_by_type(card_count_by_arena,
        #                                                                    item["legendary_chance"])
        #                     card_count_common = card_count_by_arena - card_count_rare - card_count_epic - card_count_legendary
        #
        #                     arena.update({
        #                         "card_count_by_arena": card_count_by_arena,
        #                         "card_count_common": card_count_common,
        #                         "card_count_rare": card_count_rare,
        #                         "card_count_epic": card_count_epic,
        #                         "card_count_legendary": card_count_legendary,
        #                     })
        #
        #                 item['arenas'].append(arena)
        #
        #     item['arenas'] = sorted(item['arenas'], key=lambda x: x['arena'])

        items = sorted(items, key=lambda x: x["sort_value"])
        self.save_json({
            "cycle": cycle_chests,
            "crown": crown_chests,
            "shop": shop_chests,
        }, self.json_path)

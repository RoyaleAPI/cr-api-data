"""
Card Stats
Combine multiple CSVs for a unified json file.
"""

import os

from .base import BaseGen


class Card:
    """Data about a single card."""
    def __init__(self):
        pass

class TroopCard(Card):
    """Troops, aka characters in CSVs.

    Params:
        :data: a dictionary of fields from a row in CSV.
    """
    def __init__(self, data):
        self._data = data

    @property
    def speed_en(self):
        speed = self._data.get('speed')
        if speed is None:
            return None
        speed = int(speed)
        if speed <= 45:
            return 'slow'
        if speed <= 60:
            return 'medium'
        if speed <= 90:
            return 'fast'
        if speed <= 120:
            return 'very fast'
        return None

    @property
    def dps(self):
        if not self._data.get('hit_speed'):
            return None
        if not self._data.get('damage'):
            return None
        if self._data.get('hit_speed') == 0:
            return None
        return self._data.get('damage') / self._data.get('hit_speed') * 1000

    def to_dict(self):
        data = self._data
        props = ['speed_en', 'dps']
        for prop in props:
            data[prop] = getattr(self, prop)
        return data


class CardTypes(BaseGen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exclude_fields = [
            "LoopingEffect", "OneShotEffect", "ScaledEffect", "HitEffect", "Pushback", "PushbackAll", "MinPushback",
            "MaximumTargets", "ProjectileStartHeight", "ProjectilesToCenter", "SpawnsAEO", "ControlsBuff", "Clone",
            "AttractPercentage", "HealthBar", "HealthBarOffsetY"
        ]

class Buildings(CardTypes):
    def __init__(self, config):
        super().__init__(config, id="buildings", json_id="cards_stats")


class AreaEffectsObjects(CardTypes):
    """Spells."""
    def __init__(self, config):
        super().__init__(config, id="area_effect_objects")

class Characters(CardTypes):
    """Characters."""
    def __init__(self, config):
        super().__init__(config, id="characters")


class CardStats(BaseGen):
    """Card stats"""
    def __init__(self, config):
        super().__init__(config, json_id="cards_stats")
        self.config = config
        self.exclude_fields = [
            "LoopingEffect", "OneShotEffect", "ScaledEffect", "HitEffect", "Pushback", "PushbackAll", "MinPushback",
            "MaximumTargets", "ProjectileStartHeight", "ProjectilesToCenter", "SpawnsAEO", "ControlsBuff", "Clone",
            "AttractPercentage", "HealthBar"
        ]
        self._cards_json = self.load_json(os.path.join(self.config.json.base, self.config.json.cards))

    def include_item(self, item):
        """Determine if item should be included in output."""
        if item['name'].startswith('NOTINUSE'):
            return False
        return True

    def included_items(self, items):
        """List of included items."""
        return [item for item in items if self.include_item(item)]

    def card_props(self, card_key):
        for card in self._cards_json:
            if card['name'] == card_key:
                return card
        return {}

    def inject_card_props(self, items):
        cards = []
        for item in items.copy():
            item.update(self.card_props(item['name']))
            cards.append(item)
        return cards

    def calc_hp_per_level(self, items):
        """Calculate hitpoints per level."""
        o = []
        max_levels = dict(
            Common=13,
            Rare=11,
            Epic=8,
            Legendary=5
        )
        for item in items.copy():
            hitpoints = item.get('hitpoints')
            rarity = item.get('rarity')
            hp_per_level = None
            if all([hitpoints, rarity]):
                hp_per_level = []
                hp = hitpoints
                for level in range(max_levels[rarity]):
                    # doesn’t work
                    # hp_per_level.append(hp)
                    # hp = int(hp * 1.1)

                    hp = hitpoints * (1.1 ** level)
                    hp_per_level.append(hp)

                # hp_per_level = [hp * (1.1 ** level) for level in range(max_levels[rarity])]
            item['hitpoints_per_level'] = hp_per_level
            o.append(item)
        return o




    def run(self):
        buildings = Buildings(self.config)
        buildings_data = buildings.load_csv(exclude_empty=True)
        buildings_data = self.inject_card_props(buildings_data)

        area_effect_objects = AreaEffectsObjects(self.config)
        area_effect_objects_data = area_effect_objects.load_csv()
        area_effect_objects_data = self.inject_card_props(area_effect_objects_data)

        characters = Characters(self.config)
        characters_data = characters.load_csv(exclude_empty=True)
        characters_data = self.inject_card_props(characters_data)

        troops = []
        for character_data in characters_data:
            troop = TroopCard(character_data)
            troops.append(troop.to_dict())

        troop_items = self.included_items(characters_data)
        building_items = self.included_items(buildings_data)
        spell_items = self.included_items(area_effect_objects_data)

        troop_items = self.calc_hp_per_level(troop_items)
        building_items = self.calc_hp_per_level(building_items)

        self.save_json({
            "troop": troop_items,
            "building": building_items,
            "spell": spell_items
        })



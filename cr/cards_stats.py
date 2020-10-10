"""
Card Stats
Combine multiple CSVs for a unified json file.
"""

import json
import os

from .base import BaseGen

CARDS_JSON = None


def sc_key_to_key(name):
    global CARDS_JSON
    if CARDS_JSON is None:
        with open('./docs/json/cards.json') as f:
            CARDS_JSON = json.load(f)
    for item in CARDS_JSON:
        if item.get('sc_key') == name:
            return item.get('key')
    return None


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
        super().__init__()
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
        data = self._data.copy()
        props = ['speed_en', 'dps']
        for prop in props:
            data[prop] = getattr(self, prop)

        return data


class CardTypes(BaseGen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.exclude_fields = [
        #     "LoopingEffect", "OneShotEffect", "ScaledEffect", "HitEffect", "Pushback", "PushbackAll", "MinPushback",
        #     "MaximumTargets", "ProjectileStartHeight", "ProjectilesToCenter", "SpawnsAEO", "ControlsBuff", "Clone",
        #     "AttractPercentage", "HealthBar", "HealthBarOffsetY"
        # ]


class Buildings(CardTypes):
    """Buildings."""

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


class SpellsCharacters(CardTypes):
    """Characters."""

    def __init__(self, config):
        super().__init__(config, id="spells_characters")

class SpellsBuildings(CardTypes):
    """Buildings."""

    def __init__(self, config):
        super().__init__(config, id="spells_buildings")

class SpellsOther(CardTypes):
    """Other: aka spells"""

    def __init__(self, config):
        super().__init__(config, id="spells_other")



class Projectiles(CardTypes):
    """Characters."""

    def __init__(self, config):
        super().__init__(config, id="projectiles")


class CharacterBuffs(CardTypes):
    """Characters."""

    def __init__(self, config):
        super().__init__(config, id="character_buffs")


class CardStats(BaseGen):
    """Card stats"""
    max_levels = dict(
        Common=13,
        Rare=11,
        Epic=8,
        Legendary=5,
    )

    # total hack from global
    level_multipliers = [
        1.0, # legendary
        1.1,
        1.21,
        1.33, # epic
        1.46,
        1.60,
        1.76, # rare
        1.93,
        2.12, # common
        2.33,
        2.56,
        2.81,
        3.09
    ]

    def __init__(self, config):
        super().__init__(config, json_id="cards_stats")
        self.config = config
        # self.exclude_fields = [
        #     "LoopingEffect", "OneShotEffect", "ScaledEffect", "HitEffect", "Pushback", "PushbackAll", "MinPushback",
        #     "MaximumTargets", "ProjectileStartHeight", "ProjectilesToCenter", "SpawnsAEO", "ControlsBuff", "Clone",
        #     "AttractPercentage", "HealthBar"
        # ]
        self._cards_json = self.load_json(os.path.join(self.config.json.base, self.config.json.cards))
        self._rarities = None

    def include_item(self, item):
        """Determine if item should be included in output."""
        name = item.get('name')
        if name is None:
            return False

        if name.startswith('NOTINUSE'):
            return False
        else:
            pass
            # print("Item has no name key")
            # print(item)
        return True

    def included_items(self, items):
        """List of included items."""
        return [item for item in items if self.include_item(item)]

    def card_props(self, card_key):
        for card in self._cards_json:
            if card.get('name') == card_key:
                return card
        return {}

    def inject_card_props(self, items):
        cards = []
        for item in items.copy():
            item.update(self.card_props(item.get('name')))
            cards.append(item)
        return cards

    def get_rarities_multipliers(self, rarity, level):
        if self._rarities is None:
            with open('./docs/json/rarities.json') as f:
                self._rarities = json.load(f)

        for r in self._rarities:
            if r.get('name') == rarity:
                if level == 0:
                    return 100
                return r['power_level_multiplier'][level - 1]

    def calc_per_level(self, items, section=None, per_level_section=None):
        """Calculate hitpoints per level."""
        o = []

        if not all([section, per_level_section]):
            return items

        for item in items.copy():
            value = item.get(section)
            rarity = item.get('rarity')
            per_level = None

            # skip if rarity is Hero
            if rarity == 'Hero':
                continue

            if all([value, rarity]):
                per_level = [
                    int(value * self.get_rarities_multipliers(rarity, level) / 100)
                    for level in range(self.max_levels[rarity] + 1)
                ]

            # print(section, per_level_section, per_level)

            item[per_level_section] = per_level
            o.append(item)
        return o

    def calc_dps(self, items):
        o = []
        for item in items.copy():
            if isinstance(item, dict):
                if item.get('damage') and item.get('speed'):
                    if item.get('speed', 0) > 0:
                        dps = item.get('damage') / item.get('speed') * 1000
                        # print(dps, item['damage'], item['speed'])
                        item['dps'] = int(dps)
            o.append(item)
        return o

    def add_projectile(self, items, projectiles):
        o = []
        for item in items.copy():
            p = item.get('projectile')
            if p is not None:
                for p_item in projectiles:
                    if p_item.get('name') == p:
                        item['projectile_data'] = p_item

                # copy damage_per_level over
                item['damage_per_level'] = item['projectile_data'].get('damage_per_level')

                count = item.get('summon_number') or 1
                dps_per_level = item['projectile_data'].get('dps_per_level')
                if dps_per_level is not None:
                    dps_per_level = [int(l / count) for l in dps_per_level]

                item['dps_per_level'] = dps_per_level
            o.append(item)
        return o

    def add_extended_features(self, items, name_field, feature_items):
        for item in items:
            name = item.get(name_field)
            if name:
                for f_item in feature_items:
                    if f_item.get('name') == name:
                        item[f"{name_field}_data"] = f_item
        return items

    def run(self):
        buildings = Buildings(self.config)
        buildings_data = buildings.load_csv(exclude_empty=False)
        buildings_data = self.inject_card_props(buildings_data)

        area_effect_objects = AreaEffectsObjects(self.config)
        area_effect_objects_data = area_effect_objects.load_csv()
        area_effect_objects_data = self.inject_card_props(area_effect_objects_data)

        characters = Characters(self.config)
        characters_items = characters.load_csv(exclude_empty=False)
        characters_items = self.inject_card_props(characters_items)

        spells_characters = SpellsCharacters(self.config)
        spells_characters_data = spells_characters.load_csv(exclude_empty=False)

        spells_buildings = SpellsBuildings(self.config)
        spells_buildings_data = spells_buildings.load_csv(exclude_empty=False)

        spells_other = SpellsOther(self.config)
        spells_other_data = spells_other.load_csv(exclude_empty=False)

        character_buffs = CharacterBuffs(self.config)
        character_buffs_data = character_buffs.load_csv(exclude_empty=False)

        def find_character(name):
            for item in characters_items:
                if item.get('name') == name:
                    return item
            return None

        for c in characters_items:
            for s in spells_characters_data:
                if c.get('name') == s.get('name'):
                    c.update(dict(
                        summon_character=s.get('summon_character'),
                        summon_number=s.get('summon_number') or 0,
                        summon_character_second=s.get('summon_character_second'),
                        summon_character_second_count=s.get('summon_character_second_count') or 0,
                    ))

        # building item is a dict
        for b in buildings_data:
            for s in spells_buildings_data:
                if b.get('name') == s.get('name'):
                    b.update({k:v for k, v in s.items() if k not in b.keys()})


        # spells
        for a in area_effect_objects_data:
            for s in spells_other_data:
                if a.get('name') == s.get('name'):
                    a.update({k:v for k, v in s.items() if k not in a.keys()})



        projectiles = Projectiles(self.config)
        projectiles_data = projectiles.load_csv(exclude_empty=True)
        projectiles_data = self.inject_card_props(projectiles_data)

        troops = []
        for character_data in characters_items:
        # for character_data in spells_characters_data:
            troop = TroopCard(character_data)
            troops.append(troop.to_dict())

        troop_items = self.included_items(spells_characters_data)
        building_items = self.included_items(buildings_data)
        spell_items = self.included_items(area_effect_objects_data)
        projectile_items = self.included_items(projectiles_data)
        character_buff_items = self.included_items(character_buffs_data)

        characters_items = self.calc_per_level(characters_items, 'hitpoints', 'hitpoints_per_level')
        characters_items = self.calc_per_level(characters_items, 'damage', 'damage_per_level')
        characters_items = self.calc_per_level(characters_items, 'dps', 'dps_per_level')

        troop_items = self.calc_per_level(troop_items, 'hitpoints', 'hitpoints_per_level')
        troop_items = self.calc_per_level(troop_items, 'damage', 'damage_per_level')
        troop_items = self.calc_per_level(troop_items, 'dps', 'dps_per_level')

        building_items = self.calc_per_level(building_items, 'hitpoints', 'hitpoints_per_level')
        building_items = self.calc_per_level(building_items, 'damage', 'damage_per_level')
        building_items = self.calc_per_level(building_items, 'dps', 'dps_per_level')

        spell_items = self.calc_per_level(spell_items, 'hitpoints', 'hitpoints_per_level')
        spell_items = self.calc_per_level(spell_items, 'damage', 'damage_per_level')
        spell_items = self.calc_per_level(spell_items, 'dps', 'dps_per_level')

        projectile_items = self.calc_per_level(projectile_items, 'damage', 'damage_per_level')
        projectile_items = self.calc_dps(projectile_items)
        projectile_items = self.calc_per_level(projectile_items, 'dps', 'dps_per_level')

        # add character buffs to items
        buffs = ['target_buff', 'buff']
        items_group = [
            troop_items,
            building_items,
            spell_items,
            projectile_items
        ]
        for buff in buffs:
            for items in items_group:
                items = self.add_extended_features(items, buff, character_buff_items)

        # inject projectile data
        troop_items = self.add_projectile(troop_items, projectile_items)

        # add full summon character object
        # for troop_item in troop_items:
        #     chr = troop_item.get("summon_character")
        #     if chr is not None:
        #         troop_item['summon_character_obj'] = copy.deepcopy(find_character(chr))

        # insert card keys from constants

        for items in [troop_items, building_items, spell_items]:
            for item in items:
                item['key'] = sc_key_to_key(item.get('name'))

        self.save_json({
            "troop": troop_items,
            "building": building_items,
            "spell": spell_items,
            "projectile": projectile_items,
            "characters": characters_items,
            "character_buff": character_buff_items,
        })

        # also save section specific items
        self.save_json(troop_items, json_path='./docs/json/cards_stats_troop.json')
        self.save_json(building_items, json_path='./docs/json/cards_stats_building.json')
        self.save_json(spell_items, json_path='./docs/json/cards_stats_spell.json')
        self.save_json(projectile_items, json_path='./docs/json/cards_stats_projectile.json')
        self.save_json(characters_items, json_path='./docs/json/cards_stats_characters.json')
        self.save_json(character_buff_items, json_path='./docs/json/cards_stats_character_buff.json')


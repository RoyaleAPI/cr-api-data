"""
Generate classic deck required by blog post.
"""

import json

classic_decks = [
    "Blind_Classic_RoyalHogs",
    "Blind_Classic_MegaKnight",
    "Blind_Classic_Mortar",
    "Blind_Classic_GoblinGiant",
    "Blind_Classic_Xbow",
    "Blind_Classic_LavaLoon"
]

with open('/Users/sml/git/cr-api-data/json/predefined_decks.json') as f:
    predefined_decks = json.load(f)

template = """
## {title}

{card_names}

<div
    class="ui deck embed"
    data-url="/embed/deck/name/{card_keys}"
>
</div>

"""

decks = []

for name in classic_decks:
    for deck in predefined_decks:
        if deck.get('name') == name:
            decks.append(deck)

with open('/Users/sml/git/cr-api-data/json/cards.json') as f:
    cards = json.load(f)


for deck in decks:
    card_keys = deck.get('spells')
    deck_cards = []
    for card_key in card_keys:
        for card in cards:
            if card.get('key') == card_key:
                deck_cards.append(card)
    deck['cards'] = deck_cards

def get_card(key):
    for c in cards:
        if c.get('key') == key:
            return c
    return None

# output
for deck in decks:
    deck_cards = deck.get('cards', [])
    print(template.format(
        title=deck.get('name_en'),
        card_names=", ".join([
            card.get('name') for card in deck_cards
        ]),
        card_keys=",".join([
            card.get('key') for card in deck_cards
        ]),

    ))
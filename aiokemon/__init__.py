"""
# aiokemon

aiokemon is an asynchronous Python wrapper for making PokéAPI requests.

Here is a basic usage example of getting a Pokemon:

```python
>>> import aiokemon as ak
>>> breloom = await ak.pokemon('breloom')
>>> breloom
<pokemon-breloom>
>>> breloom.abilities[0].ability.name
'effect-spore'
>>> breloom.attrs # shows PokéAPI data attributes
['abilities', 'base_experience', 'forms', 'game_indices', 'height',
'held_items', 'id', 'is_default', 'location_area_encounters', 'moves', 'name',
'order', 'past_types', 'species', 'sprites', 'stats', 'types', 'url', 'weight']
```

Above is the recommended usage because specific endpoint functions fully
support type hinting. However, if you need the ability to pass the endpoint
as an argument, you can do it like so:

```python
>>> import aiokemon as ak
>>> breloom = await ak.PokeAPIResource.get_resource('pokemon', 'breloom')
>>> breloom
<pokemon-breloom>
...
```

While aiokemon has no official docs, it is a wrapper library made to mimic
PokéAPI's endpoints and typing almost exactly. In fact, the Python code found
in the aiokemon.endpoints.* packages is literally scraped from the PokéAPI
docs page's HTML and formatted into Python (see aiokemon/scraper.py).

For more details about aiokemon, check the [github](https://github.com/bday-boy/aiokemon).

For more details about PokéAPI's documentation, check the official [PokéAPI docs page](https://pokeapi.co/docs/v2).
"""


from aiokemon.endpoints import *
from aiokemon.core.api import PokeAPIResource
from aiokemon.core.loaders import *

__all__ = [
    # Broad API functionality
    'PokeAPIResource',

    # Resource-specific functions (recommended use)
    'berry',
    'berry_firmness',
    'berry_flavor',
    'contest_type',
    'contest_effect',
    'super_contest_effect',
    'encounter_method',
    'encounter_condition',
    'encounter_condition_value',
    'evolution_chain',
    'evolution_trigger',
    'generation',
    'pokedex',
    'version',
    'version_group',
    'item',
    'item_attribute',
    'item_category',
    'item_fling_effect',
    'item_pocket',
    'machine',
    'move',
    'move_ailment',
    'move_battle_style',
    'move_category',
    'move_damage_class',
    'move_learn_method',
    'move_target',
    'location',
    'location_area',
    'pal_park_area',
    'region',
    'ability',
    'characteristic',
    'egg_group',
    'gender',
    'growth_rate',
    'nature',
    'pokeathlon_stat',
    'pokemon',
    'pokemon_color',
    'pokemon_form',
    'pokemon_habitat',
    'pokemon_shape',
    'pokemon_species',
    'stat',
    'type_',
    'language',

    # Classes for type hinting
    'Berry',
    'BerryFirmness',
    'BerryFlavor',
    'ContestType',
    'ContestEffect',
    'SuperContestEffect',
    'EncounterMethod',
    'EncounterCondition',
    'EncounterConditionValue',
    'EvolutionChain',
    'EvolutionTrigger',
    'Generation',
    'Pokedex',
    'Version',
    'VersionGroup',
    'Item',
    'ItemAttribute',
    'ItemCategory',
    'ItemFlingEffect',
    'ItemPocket',
    'Location',
    'LocationArea',
    'PalParkArea',
    'Region',
    'Machine',
    'Move',
    'MoveAilment',
    'MoveBattleStyle',
    'MoveCategory',
    'MoveDamageClass',
    'MoveLearnMethod',
    'MoveTarget',
    'Ability',
    'Characteristic',
    'EggGroup',
    'Gender',
    'GrowthRate',
    'Nature',
    'PokeathlonStat',
    'Pokemon',
    'LocationAreaEncounter',
    'PokemonColor',
    'PokemonForm',
    'PokemonHabitat',
    'PokemonShape',
    'PokemonSpecies',
    'Stat',
    'Type',
    'Language'
]

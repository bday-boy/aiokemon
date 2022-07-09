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

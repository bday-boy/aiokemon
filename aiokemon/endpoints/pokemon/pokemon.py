# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class PokemonType:
    slot: int
    type: NamedAPIResource


class PokemonSprites:
    front_default: str
    front_shiny: str
    front_female: str
    front_shiny_female: str
    back_default: str
    back_shiny: str
    back_female: str
    back_shiny_female: str


class PokemonStat:
    stat: NamedAPIResource
    effort: int
    base_stat: int


class PokemonMoveVersion:
    move_learn_method: NamedAPIResource
    version_group: NamedAPIResource
    level_learned_at: int


class PokemonMove:
    move: NamedAPIResource
    version_group_details: List[PokemonMoveVersion]


class PokemonHeldItemVersion:
    version: NamedAPIResource
    rarity: int


class PokemonHeldItem:
    item: NamedAPIResource
    version_details: List[PokemonHeldItemVersion]


class PokemonTypePast:
    generation: NamedAPIResource
    types: List[PokemonType]


class PokemonFormType:
    slot: int
    type: NamedAPIResource


class PokemonAbility:
    is_hidden: bool
    slot: int
    ability: NamedAPIResource


class Pokemon(PokeAPIResource):
    id: int
    name: str
    base_experience: int
    height: int
    is_default: bool
    order: int
    weight: int
    abilities: List[PokemonAbility]
    forms: List[NamedAPIResource]
    game_indices: List[VersionGameIndex]
    held_items: List[PokemonHeldItem]
    location_area_encounters: str
    moves: List[PokemonMove]
    past_types: List[PokemonTypePast]
    sprites: PokemonSprites
    species: NamedAPIResource
    stats: List[PokemonStat]
    types: List[PokemonType]

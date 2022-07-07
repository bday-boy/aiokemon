from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import NamedAPIResource, VersionGameIndex
from aiokemon.endpoints.sprite import PokemonSprites


class PokemonAbility:
    """An ability entry in a Pokemon's abilities array."""
    is_hidden: bool
    slot: int
    ability: NamedAPIResource


class PokemonHeldItemVersion:
    """A single version_details entry."""
    version: NamedAPIResource
    rarity: int


class PokemonHeldItem:
    """A held item entry in a Pokemon's held_items array."""
    item: NamedAPIResource
    version_details: List[PokemonHeldItemVersion]


class PokemonMoveVersion:
    """A version group detail entry in a move's version_group_details array."""
    move_learn_method: NamedAPIResource
    version_group: NamedAPIResource
    level_learned_at: int


class PokemonMove:
    """A move entry in a Pokemon's moves array."""
    move: NamedAPIResource
    version_group_details: List[PokemonMoveVersion]


class PokemonStat:
    """A stat entry in a Pokemon's stats array."""
    stat: NamedAPIResource
    effort: int
    base_stat: int


class PokemonType:
    """A type entry in a Pokemon's types array."""
    slot: int
    type: NamedAPIResource


class PokemonTypePast:
    """A Pokemon's past types."""
    generation: NamedAPIResource
    types: List[PokemonType]


class Pokemon(PokeAPIResource):
    """A pokemon endpoint resource."""
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

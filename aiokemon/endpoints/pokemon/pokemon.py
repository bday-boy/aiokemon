from typing import List

from aiokemon.core.api import APIResource
from aiokemon.endpoints.common import SimpleSubResource, GameIndex
from aiokemon.endpoints.sprite import Sprite


class Ability:
    """An ability entry in a Pokemon's abilities array."""
    ability: SimpleSubResource
    is_hidden: bool
    slot: int


class VersionDetail:
    """A single version_details entry."""
    rarity: int
    version: SimpleSubResource


class HeldItem:
    """A held item entry in a Pokemon's held_items array."""
    item: SimpleSubResource
    version_details: List[VersionDetail]


class VersionGroupDetail:
    """A version group detail entry in a move's version_group_details array."""
    level_learned_at: int
    move_learn_method: SimpleSubResource
    version_group: SimpleSubResource


class Move:
    """A move entry in a Pokemon's moves array."""
    move: SimpleSubResource
    version_group_details: List[VersionGroupDetail]


class Stat:
    """A stat entry in a Pokemon's stats array."""
    base_stat: int
    effort: int
    stat: SimpleSubResource


class Type:
    """A type entry in a Pokemon's types array."""
    slot: int
    type: SimpleSubResource


class Pokemon(APIResource):
    """A pokemon endpoint resource."""
    abilities: List[Ability]
    base_experience: int
    forms: List[SimpleSubResource]
    game_indices: List[GameIndex]
    height: int
    held_items: List[HeldItem]
    id: int
    is_default: bool
    location_area_encounters: str
    moves: List[Move]
    name: str
    order: int
    past_types: List
    species: SimpleSubResource
    sprites: Sprite
    stats: List[Stat]
    types: List[SimpleSubResource]
    weight: int

from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import APIResource, NamedAPIResource, Name


class MoveStatAffect:
    """How a move affects a stat."""
    change: int
    move: NamedAPIResource


class MoveStatAffectSets:
    """Contains lists of moves that increase or decrease a stat."""
    increase: List[MoveStatAffect]
    decrease: List[MoveStatAffect]


class NatureStatAffectSets:
    """Contains lists of natures that increase or decrease a stat."""
    increase: List[NamedAPIResource]
    decrease: List[NamedAPIResource]


class Stat(PokeAPIResource):
    """A stat endpoint resource."""
    id: int
    name: str
    game_index: int
    is_battle_only: bool
    affecting_moves: MoveStatAffectSets
    affecting_natures: NatureStatAffectSets
    characteristics: APIResource
    move_damage_class: NamedAPIResource
    names: List[Name]

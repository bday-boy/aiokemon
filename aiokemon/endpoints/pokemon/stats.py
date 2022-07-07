# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class NatureStatAffectSets:
    increase: List[NamedAPIResource]
    decrease: List[NamedAPIResource]


class MoveStatAffect:
    change: int
    move: NamedAPIResource


class MoveStatAffectSets:
    increase: List[MoveStatAffect]
    decrease: List[MoveStatAffect]


class Stat(PokeAPIResource):
    id: int
    name: str
    game_index: int
    is_battle_only: bool
    affecting_moves: MoveStatAffectSets
    affecting_natures: NatureStatAffectSets
    characteristics: List[APIResource]
    move_damage_class: NamedAPIResource
    names: List[Name]

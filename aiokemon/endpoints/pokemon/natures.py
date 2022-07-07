# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class MoveBattleStylePreference:
    low_hp_preference: int
    high_hp_preference: int
    move_battle_style: NamedAPIResource


class NatureStatChange:
    max_change: int
    pokeathlon_stat: NamedAPIResource


class Nature(PokeAPIResource):
    id: int
    name: str
    decreased_stat: NamedAPIResource
    increased_stat: NamedAPIResource
    hates_flavor: NamedAPIResource
    likes_flavor: NamedAPIResource
    pokeathlon_stat_changes: List[NatureStatChange]
    move_battle_style_preferences: List[MoveBattleStylePreference]
    names: List[Name]

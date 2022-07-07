# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class EvolutionDetail:
    item: NamedAPIResource
    trigger: NamedAPIResource
    gender: int
    held_item: NamedAPIResource
    known_move: NamedAPIResource
    known_move_type: NamedAPIResource
    location: NamedAPIResource
    min_level: int
    min_happiness: int
    min_beauty: int
    min_affection: int
    needs_overworld_rain: bool
    party_species: NamedAPIResource
    party_type: NamedAPIResource
    relative_physical_stats: int
    time_of_day: str
    trade_species: NamedAPIResource
    turn_upside_down: bool


class ChainLink:
    is_baby: bool
    species: NamedAPIResource
    evolution_details: List[EvolutionDetail]
    evolves_to: List['ChainLink']


class EvolutionChain(PokeAPIResource):
    id: int
    baby_trigger_item: NamedAPIResource
    chain: ChainLink

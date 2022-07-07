# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class PalParkEncounterSpecies:
    base_score: int
    rate: int
    pokemon_species: NamedAPIResource


class PalParkArea(PokeAPIResource):
    id: int
    name: str
    names: List[Name]
    pokemon_encounters: List[PalParkEncounterSpecies]

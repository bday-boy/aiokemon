# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class GrowthRateExperienceLevel:
    level: int
    experience: int


class GrowthRate(PokeAPIResource):
    id: int
    name: str
    formula: str
    descriptions: List[Description]
    levels: List[GrowthRateExperienceLevel]
    pokemon_species: List[NamedAPIResource]

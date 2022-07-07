# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class Location(PokeAPIResource):
    id: int
    name: str
    region: NamedAPIResource
    names: List[Name]
    game_indices: List[GenerationGameIndex]
    areas: List[NamedAPIResource]

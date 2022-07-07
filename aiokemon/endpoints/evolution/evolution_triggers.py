# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class EvolutionTrigger(PokeAPIResource):
    id: int
    name: str
    names: List[Name]
    pokemon_species: List[NamedAPIResource]

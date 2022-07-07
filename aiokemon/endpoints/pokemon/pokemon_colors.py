# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class PokemonColor(PokeAPIResource):
    id: int
    name: str
    names: List[Name]
    pokemon_species: List[NamedAPIResource]

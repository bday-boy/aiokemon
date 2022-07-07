# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class Generation(PokeAPIResource):
    id: int
    name: str
    abilities: List[NamedAPIResource]
    names: List[Name]
    main_region: NamedAPIResource
    moves: List[NamedAPIResource]
    pokemon_species: List[NamedAPIResource]
    types: List[NamedAPIResource]
    version_groups: List[NamedAPIResource]

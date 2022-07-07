# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class Region(PokeAPIResource):
    id: int
    locations: List[NamedAPIResource]
    name: str
    names: List[Name]
    main_generation: NamedAPIResource
    pokedexes: List[NamedAPIResource]
    version_groups: List[NamedAPIResource]

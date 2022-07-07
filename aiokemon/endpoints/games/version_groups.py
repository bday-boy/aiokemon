# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class VersionGroup(PokeAPIResource):
    id: int
    name: str
    order: int
    generation: NamedAPIResource
    move_learn_methods: List[NamedAPIResource]
    pokedexes: List[NamedAPIResource]
    regions: List[NamedAPIResource]
    versions: List[NamedAPIResource]

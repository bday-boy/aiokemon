# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class BerryFirmness(PokeAPIResource):
    id: int
    name: str
    berries: List[NamedAPIResource]
    names: List[Name]

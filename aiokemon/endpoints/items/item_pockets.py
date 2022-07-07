# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class ItemPocket(PokeAPIResource):
    id: int
    name: str
    categories: List[NamedAPIResource]
    names: List[Name]

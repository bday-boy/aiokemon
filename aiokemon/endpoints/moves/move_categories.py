# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class MoveCategory(PokeAPIResource):
    id: int
    name: str
    moves: List[NamedAPIResource]
    descriptions: List[Description]

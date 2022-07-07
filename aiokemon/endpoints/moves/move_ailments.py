# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class MoveAilment(PokeAPIResource):
    id: int
    name: str
    moves: List[NamedAPIResource]
    names: List[Name]

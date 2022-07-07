# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class MoveAilment(PokeAPIResource):
    id: int
    name: str
    moves: List[NamedAPIResource]
    names: List[Name]

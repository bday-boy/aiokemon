# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class MoveTarget(PokeAPIResource):
    id: int
    name: str
    descriptions: List[Description]
    moves: List[NamedAPIResource]
    names: List[Name]

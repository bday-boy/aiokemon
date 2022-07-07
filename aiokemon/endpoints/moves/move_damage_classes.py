# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class MoveDamageClass(PokeAPIResource):
    id: int
    name: str
    descriptions: List[Description]
    moves: List[NamedAPIResource]
    names: List[Name]

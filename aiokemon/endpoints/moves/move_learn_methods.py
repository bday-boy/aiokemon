# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class MoveLearnMethod(PokeAPIResource):
    id: int
    name: str
    descriptions: List[Description]
    names: List[Name]
    version_groups: List[NamedAPIResource]

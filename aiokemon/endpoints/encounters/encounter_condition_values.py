# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class EncounterConditionValue(PokeAPIResource):
    id: int
    name: str
    condition: NamedAPIResource
    names: List[Name]

# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class EncounterMethod(PokeAPIResource):
    id: int
    name: str
    order: int
    names: List[Name]

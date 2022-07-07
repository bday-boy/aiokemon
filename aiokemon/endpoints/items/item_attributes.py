# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class ItemAttribute(PokeAPIResource):
    id: int
    name: str
    items: List[NamedAPIResource]
    names: List[Name]
    descriptions: List[Description]

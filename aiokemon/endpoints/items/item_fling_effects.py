# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class ItemFlingEffect(PokeAPIResource):
    id: int
    name: str
    effect_entries: List[Effect]
    items: List[NamedAPIResource]

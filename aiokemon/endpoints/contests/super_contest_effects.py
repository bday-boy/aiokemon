# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class SuperContestEffect(PokeAPIResource):
    id: int
    appeal: int
    flavor_text_entries: List[FlavorText]
    moves: List[NamedAPIResource]

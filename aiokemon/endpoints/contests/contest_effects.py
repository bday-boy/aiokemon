# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class ContestEffect(PokeAPIResource):
    id: int
    appeal: int
    jam: int
    effect_entries: List[Effect]
    flavor_text_entries: List[FlavorText]

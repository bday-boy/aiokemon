# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class BerryFlavorMap:
    potency: int
    flavor: NamedAPIResource


class Berry(PokeAPIResource):
    id: int
    name: str
    growth_time: int
    max_harvest: int
    natural_gift_power: int
    size: int
    smoothness: int
    soil_dryness: int
    firmness: NamedAPIResource
    flavors: List[BerryFlavorMap]
    item: NamedAPIResource
    natural_gift_type: NamedAPIResource

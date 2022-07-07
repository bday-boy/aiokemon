# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class FlavorBerryMap:
    potency: int
    berry: NamedAPIResource


class BerryFlavor(PokeAPIResource):
    id: int
    name: str
    berries: List[FlavorBerryMap]
    contest_type: NamedAPIResource
    names: List[Name]

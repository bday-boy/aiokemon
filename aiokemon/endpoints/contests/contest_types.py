# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class ContestName:
    name: str
    color: str
    language: NamedAPIResource


class ContestType(PokeAPIResource):
    id: int
    name: str
    berry_flavor: NamedAPIResource
    names: List[ContestName]

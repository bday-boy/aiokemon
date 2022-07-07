# This file was generated automatically.
from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class Machine(PokeAPIResource):
    id: int
    item: NamedAPIResource
    move: NamedAPIResource
    version_group: NamedAPIResource

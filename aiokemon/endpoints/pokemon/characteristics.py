# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class Characteristic(PokeAPIResource):
    id: int
    gene_modulo: int
    possible_values: List[int]

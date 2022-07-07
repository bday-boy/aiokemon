from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class Language:
    id: int
    name: str
    official: bool
    iso639: str
    iso3166: str
    names: List[Name]

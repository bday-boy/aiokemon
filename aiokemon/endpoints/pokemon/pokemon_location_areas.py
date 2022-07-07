# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class LocationAreaEncounter(PokeAPIResource):
    location_area: NamedAPIResource
    version_details: List[VersionEncounterDetail]

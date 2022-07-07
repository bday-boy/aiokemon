# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class PokemonEncounter:
    pokemon: NamedAPIResource
    version_details: List[VersionEncounterDetail]


class EncounterVersionDetails:
    rate: int
    version: NamedAPIResource


class EncounterMethodRate:
    encounter_method: NamedAPIResource
    version_details: List[EncounterVersionDetails]


class LocationArea(PokeAPIResource):
    id: int
    name: str
    game_index: int
    encounter_method_rates: List[EncounterMethodRate]
    location: NamedAPIResource
    names: List[Name]
    pokemon_encounters: List[PokemonEncounter]

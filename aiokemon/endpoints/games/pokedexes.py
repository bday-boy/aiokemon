# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class PokemonEntry:
    entry_number: int
    pokemon_species: NamedAPIResource


class Pokedex(PokeAPIResource):
    id: int
    name: str
    is_main_series: bool
    descriptions: List[Description]
    names: List[Name]
    pokemon_entries: List[PokemonEntry]
    region: NamedAPIResource
    version_groups: List[NamedAPIResource]

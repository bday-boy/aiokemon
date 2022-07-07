# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class PokemonSpeciesGender:
    rate: int
    pokemon_species: NamedAPIResource


class Gender(PokeAPIResource):
    id: int
    name: str
    pokemon_species_details: List[PokemonSpeciesGender]
    required_for_evolution: List[NamedAPIResource]

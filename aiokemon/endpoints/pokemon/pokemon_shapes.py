# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class AwesomeName:
    awesome_name: str
    language: NamedAPIResource


class PokemonShape(PokeAPIResource):
    id: int
    name: str
    awesome_names: List[AwesomeName]
    names: List[Name]
    pokemon_species: List[NamedAPIResource]

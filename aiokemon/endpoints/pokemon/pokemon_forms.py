# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class PokemonFormSprites:
    front_default: str
    front_shiny: str
    back_default: str
    back_shiny: str


class PokemonForm(PokeAPIResource):
    id: int
    name: str
    order: int
    form_order: int
    is_default: bool
    is_battle_only: bool
    is_mega: bool
    form_name: str
    pokemon: NamedAPIResource
    types: List[PokemonFormType]
    sprites: PokemonFormSprites
    version_group: NamedAPIResource
    names: List[Name]
    form_names: List[Name]

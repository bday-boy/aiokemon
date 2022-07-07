# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class ItemHolderPokemonVersionDetail:
    rarity: int
    version: NamedAPIResource


class ItemHolderPokemon:
    pokemon: NamedAPIResource
    version_details: List[ItemHolderPokemonVersionDetail]


class ItemSprites:
    default: str


class Item(PokeAPIResource):
    id: int
    name: str
    cost: int
    fling_power: int
    fling_effect: NamedAPIResource
    attributes: List[NamedAPIResource]
    category: NamedAPIResource
    effect_entries: List[VerboseEffect]
    flavor_text_entries: List[VersionGroupFlavorText]
    game_indices: List[GenerationGameIndex]
    names: List[Name]
    sprites: ItemSprites
    held_by_pokemon: List[ItemHolderPokemon]
    baby_trigger_for: APIResource
    machines: List[MachineVersionDetail]

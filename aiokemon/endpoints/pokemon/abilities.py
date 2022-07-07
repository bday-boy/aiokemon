# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class AbilityPokemon:
    is_hidden: bool
    slot: int
    pokemon: NamedAPIResource


class AbilityFlavorText:
    flavor_text: str
    language: NamedAPIResource
    version_group: NamedAPIResource


class AbilityEffectChange:
    effect_entries: List[Effect]
    version_group: NamedAPIResource


class Ability(PokeAPIResource):
    id: int
    name: str
    is_main_series: bool
    generation: NamedAPIResource
    names: List[Name]
    effect_entries: List[VerboseEffect]
    effect_changes: List[AbilityEffectChange]
    flavor_text_entries: List[AbilityFlavorText]
    pokemon: List[AbilityPokemon]

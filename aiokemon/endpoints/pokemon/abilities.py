from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import NamedAPIResource, Name, VerboseEffect, \
    Effect


class AbilityEffectChange:
    """Effects caused by a given ability."""
    effect_entries: List[Effect]
    version_group: NamedAPIResource


class AbilityFlavorText:
    """Flavor text for an ability in a version group in a given language."""
    flavor_text: str
    language: NamedAPIResource
    version_group: NamedAPIResource


class AbilityPokemon:
    """Information for a Pokemon that has the given ability."""
    is_hidden: bool
    slot: int
    pokemon: NamedAPIResource


class Ability(PokeAPIResource):
    """An ability endpoint resource."""
    id: int
    name: str
    is_main_series: bool
    generation: NamedAPIResource
    names: List[Name]
    effect_entries: List[VerboseEffect]
    effect_changes: List[AbilityEffectChange]
    flavor_text_entries: List[AbilityFlavorText]
    pokemon: List[AbilityPokemon]

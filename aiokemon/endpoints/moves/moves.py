# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *
from aiokemon.endpoints.pokemon.abilities import AbilityEffectChange


class PastMoveStatValues:
    accuracy: int
    effect_chance: int
    power: int
    pp: int
    effect_entries: List[VerboseEffect]
    type: NamedAPIResource
    version_group: NamedAPIResource


class MoveStatChange:
    change: int
    stat: NamedAPIResource


class MoveMetaData:
    ailment: NamedAPIResource
    category: NamedAPIResource
    min_hits: int
    max_hits: int
    min_turns: int
    max_turns: int
    drain: int
    healing: int
    crit_rate: int
    ailment_chance: int
    flinch_chance: int
    stat_chance: int


class MoveFlavorText:
    flavor_text: str
    language: NamedAPIResource
    version_group: NamedAPIResource


class ContestComboDetail:
    use_before: List[NamedAPIResource]
    use_after: List[NamedAPIResource]


class ContestComboSets:
    normal: ContestComboDetail
    super: ContestComboDetail


class Move(PokeAPIResource):
    id: int
    name: str
    accuracy: int
    effect_chance: int
    pp: int
    priority: int
    power: int
    contest_combos: ContestComboSets
    contest_type: NamedAPIResource
    contest_effect: APIResource
    damage_class: NamedAPIResource
    effect_entries: List[VerboseEffect]
    effect_changes: List[AbilityEffectChange]
    learned_by_pokemon: List[NamedAPIResource]
    flavor_text_entries: List[MoveFlavorText]
    generation: NamedAPIResource
    machines: List[MachineVersionDetail]
    meta: MoveMetaData
    names: List[Name]
    past_values: List[PastMoveStatValues]
    stat_changes: List[MoveStatChange]
    super_contest_effect: APIResource
    target: NamedAPIResource
    type: NamedAPIResource

# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.common import *


class TypeRelations:
    no_damage_to: List[NamedAPIResource]
    half_damage_to: List[NamedAPIResource]
    double_damage_to: List[NamedAPIResource]
    no_damage_from: List[NamedAPIResource]
    half_damage_from: List[NamedAPIResource]
    double_damage_from: List[NamedAPIResource]


class TypeRelationsPast:
    generation: NamedAPIResource
    damage_relations: TypeRelations


class TypePokemon:
    slot: int
    pokemon: NamedAPIResource


class Type(PokeAPIResource):
    id: int
    name: str
    damage_relations: TypeRelations
    past_damage_relations: List[TypeRelationsPast]
    game_indices: List[GenerationGameIndex]
    generation: NamedAPIResource
    move_damage_class: NamedAPIResource
    names: List[Name]
    pokemon: List[TypePokemon]
    moves: List[NamedAPIResource]

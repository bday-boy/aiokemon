from typing import List

from aiokemon.core.api import APIResource
from aiokemon.endpoints.common import NamedAPIResource, GenerationGameIndex, \
    Name


class TypePokemon:
    """A single Pokemon and their type slot."""
    slot: int
    pokemon: NamedAPIResource


class TypeRelations:
    """A type's damage_relations."""
    double_damage_from: List[NamedAPIResource]
    double_damage_to: List[NamedAPIResource]
    half_damage_from: List[NamedAPIResource]
    half_damage_to: List[NamedAPIResource]
    no_damage_from: List[NamedAPIResource]
    no_damage_to: List[NamedAPIResource]


class TypeRelationsPast:
    """The damage_relations for a previous generation."""
    damage_relations: TypeRelations
    generation: NamedAPIResource


class Type(APIResource):
    """A type endpoint resource."""
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

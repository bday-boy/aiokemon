from typing import List

from aiokemon.endpoints.common import SimpleSubResource, GameIndex


class DamageRelations:
    """A type's damage_relations."""
    double_damage_from: List[SimpleSubResource]
    double_damage_to: List[SimpleSubResource]
    half_damage_from: List[SimpleSubResource]
    half_damage_to: List[SimpleSubResource]
    no_damage_from: List[SimpleSubResource]
    no_damage_to: List[SimpleSubResource]


class Name:
    """A single names entry containing a name in a given language."""
    language: SimpleSubResource
    name: str


class PastDamageRelation:
    """The damage_relations for a previous generation."""
    damage_relations: DamageRelations
    generation: SimpleSubResource


class PokemonType:
    """A single Pokemon and their type slot."""
    pokemon: SimpleSubResource
    slot: int


class Type:
    """A type endpoint resource."""
    damage_relations: DamageRelations
    game_indices: List[GameIndex]
    generation: object
    id: int
    move_damage_class: SimpleSubResource
    moves: List[SimpleSubResource]
    name: str
    names: List[Name]
    past_damage_relations: List[PastDamageRelation]
    pokemon: List[PokemonType]

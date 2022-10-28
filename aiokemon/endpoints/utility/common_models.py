from typing import List
from aiokemon.core.api import PokeAPIMetaData


class APIResource:
    """Basically a wrapper for just a URL."""
    url: str


class NamedAPIResource(PokeAPIMetaData):
    """The simplest subresource possible, containing just a name and URL."""
    name: str
    url: str


class Description:
    """An object's description in a given language."""
    description: str
    language: NamedAPIResource


class Effect:
    """An object's effect in a given language."""
    effect: str
    language: NamedAPIResource


class Encounter:
    """Encounter information about a Pokemon."""
    min_level: int
    max_level: int
    condition_values: List[NamedAPIResource]
    chance: int
    method: NamedAPIResource


class FlavorText:
    """An object's flavor text in a given language."""
    flavor_text: str
    language: NamedAPIResource
    version: NamedAPIResource


class GenerationGameIndex:
    """A game index entry in a game_indices array."""
    game_index: int
    version: NamedAPIResource


class MachineVersionDetail:
    """TM game version information."""
    machine: APIResource
    version_group: NamedAPIResource


class Name:
    """A single names entry containing a name in a given language."""
    name: str
    language: NamedAPIResource


class VerboseEffect:
    """An object's effect in a given language as well as a briefer version."""
    effect: str
    short_effect: str
    language: NamedAPIResource


class VersionEncounterDetail:
    """Encounter data about a given area in a given game."""
    version: NamedAPIResource
    max_chance: int
    encounter_details: List[Encounter]


class VersionGameIndex:
    """The internal ID of a resource with this version."""
    game_index: int
    version: NamedAPIResource


class VersionGroupFlavorText:
    """Version-specific flavor text in a given language."""
    text: str
    language: NamedAPIResource
    version_group: NamedAPIResource

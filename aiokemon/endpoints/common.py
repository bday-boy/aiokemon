from aiokemon.core.api import APIMetaData


class NamedAPIResource(APIMetaData):
    """The simplest subresource possible, containing just a name and URL."""
    name: str
    url: str


class GenerationGameIndex:
    """A game index entry in a game_indices array."""
    game_index: int
    version: NamedAPIResource


class Name:
    """A single names entry containing a name in a given language."""
    name: str
    language: NamedAPIResource

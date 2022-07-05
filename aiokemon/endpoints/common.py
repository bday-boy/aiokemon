from aiokemon.api import APIResource, APIMetaData


class SimpleSubResource(APIMetaData):
    """The simplest subresource possible, containing just a name and URL."""
    name: str
    url: str


class GameIndex:
    """A game index entry in a game_indices array."""
    game_index: int
    version: SimpleSubResource

from aiokemon.api import APIResource, APIMetaData


class SimpleSubResource(APIMetaData):
    """The simplest subresource possible, containing just a name and URL."""
    name: str
    url: str

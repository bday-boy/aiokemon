from typing import Union


class BaseSprite:
    """The base sprite subresource in the pokemon endpoint."""
    front_default: str
    front_shiny: str
    front_female: Union[str, None]
    front_shiny_female: Union[str, None]
    back_default: str
    back_shiny: str
    back_female: Union[str, None]
    back_shiny_female: Union[str, None]
    other: type
    versions: type


class DreamWorld:
    """A Pokemon's dream world artwork."""
    front_default: Union[str, None]
    front_female: Union[str, None]


class Home:
    """A Pokemon's Pokemon Home artwork."""
    front_default: str
    front_female: Union[str, None]
    front_shiny: str
    front_shiny_female: Union[str, None]


class OfficialArtwork:
    """A Pokemon's official artwork."""
    front_default: str


class Other:
    """A Pokemon's non-sprite artwork."""
    dream_world: DreamWorld
    home: Home
    official_artwork: OfficialArtwork


class PokemonSprites(BaseSprite):
    """A pokemon endpoint's sprite data."""
    other: Other

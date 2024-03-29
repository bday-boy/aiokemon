import keyword
from typing import Any, List, Optional, Union

import aiokemon.core.common as cmn


def sanitize_attribute(attr: str) -> str:
    """Given a string, this function attempts to create a valid python
    identifier by replacing all hyphens with underscores. If the given string
    is a reserved Python keyword or a built-in function, a trailing underscore
    is added (i.e. `True` -> `True_`).

    ## Raises
    `ValueError` when `attr` is not a valid identifier after replacing all
    hyphens with underscores.
    """
    attr = attr.replace('-', '_')
    if not attr.isidentifier():
        raise ValueError(f'attr "{attr}" is not a valid identifier.')
    if keyword.iskeyword(attr):
        print(
            f'Warning: string "{attr}" is a keyword. Adding a trailing '
            'underscore to prevent syntax errors.'
        )
        return attr + '_'
    return attr


class PokeAPIBase:
    """Base class containing mostly convenience functions."""

    def _safe_update(self, data: dict) -> None:
        """Sanitizes all data keys so that they are valid Python
        identifiers and converts all sub-dicts into APIMetaData and all
        sub-lists into APIMetaData lists.
        """
        for k, v in data.items():
            k = sanitize_attribute(k)
            self.__dict__[k] = new_pokeapimetadata(k, v)

    @property
    def pokeapi_attrs(self) -> List[str]:
        """Returns all PokéAPI attributes of the class."""
        return [
            k for k in dir(self) if not k.startswith('_')
            and k not in {'pokeapi_attrs', 'as_resource'}
        ]


class PokeAPIResource(PokeAPIBase):
    """Class-attribute-based wrapper for an API. Initializes all dictionary
    key-value pairs from a JSON response as class attributes.

    All class attributes that are reserved Python keywords will have a
    trailing underscore added, because Python would throw a SyntaxError
    without it. Example:
    ```python
    class A(): pass
    a = A()
    setattr(a, 'True', 10)  # No error
    a.True                  # SyntaxError
    setattr(a, 'True_', 10) # No error
    a.True_                 # Gets 10
    ```
    """

    def __init__(self, endpoint: str, data: dict, custom: Optional[dict] = None) -> None:
        """Creates an un-loaded APIResource class. Attributes and such can
        only be guaranteed once the async function _load is awaited.
        """
        self._safe_update(data)
        self._endpoint = endpoint
        self.name = data.get('name')
        self.id = data.get('id')
        if custom is not None:
            self._safe_update(custom)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<{self._endpoint} {self.name}>'


class PokeAPIMetaData(PokeAPIBase):
    """Simple class used for sub-dicts and -lists in a response JSON."""

    def __init__(self, key: str, data: dict) -> None:
        self._key = key
        self._safe_update(data)

    @property
    def is_resource(self) -> bool:
        return bool(getattr(self, 'url', None))

    async def as_resource(self, session, raise_error: bool = False,
                          ) -> Union[PokeAPIResource, None]:
        """Creates a new APIResource based on the URL from this class. If
        raise_error is false, AttributeError will not be raised even if the
        PokeAPIMetaData cannot be loaded as a resource.

        ## Raises
        `AttributeError` if a PokeAPIMetaData cannot be loaded as a resource.
        """
        if self.is_resource:
            url = getattr(self, 'url')
            json_data = await session.get_json(url)
            endpoint, _ = cmn.break_url(url)
            return PokeAPIResource(endpoint, json_data)
        elif raise_error:
            raise AttributeError(
                f'object {repr(self)} has no attribute "url" and thus cannot '
                'be loaded as a resource'
            )
        else:
            return None

    def __str__(self) -> str:
        return self._key

    def __repr__(self) -> str:
        return f'<APIMetaData object for key "{self._key}">'


def new_pokeapimetadata(key: str, obj: Any) -> Any:
    """Turns a dict or list of dicts into an APIMetaData object or a list of
    APIMetaData objects and does nothing otherwise.
    """
    if isinstance(obj, dict):
        return PokeAPIMetaData(key, obj)
    elif isinstance(obj, list) and all(isinstance(item, dict) for item in obj):
        return [PokeAPIMetaData(key, item) for item in obj]
    else:
        return obj

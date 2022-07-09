from typing import Any, List, Optional, Type, Union

import aiokemon.core.common as cmn
import aiokemon.core.matcher as matcher
from aiokemon.core.common import Resource


class PokeAPIBase:
    """Base class containing mostly convenience functions."""

    def _safe_update(self, data: dict) -> None:
        """Sanitizes all data keys so that they are valid Python
        identifiers and converts all sub-dicts into APIMetaData and all
        sub-lists into APIMetaData lists.
        """
        for k, v in data.items():
            k = cmn.sanitize_attribute(k)
            self.__dict__[k] = make_object(k, v)

    @property
    def attrs(self) -> List[str]:
        """Returns all PokéAPI attributes of the class."""
        return [
            k for k in dir(self) if not k.startswith('_')
            and k not in {'attrs', 'as_resource'}
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

    def __init__(self, endpoint: str, resource: Resource,
                 custom: Optional[dict] = None) -> None:
        """Creates an un-loaded APIResource class. Attributes and such can
        only be guaranteed once the async function _load is awaited.
        """
        if custom is not None:
            self._safe_update(custom)
        self._endpoint = endpoint
        self._resource = resource
        self._loaded = False

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<{self._endpoint}-{self._resource}>'

    async def _load(self) -> None:
        """Asynchronously loads the information for the given resource
        in-place and returns a reference to itself.
        """
        if isinstance(self._resource, str):
            self._resource = await matcher.best_match(
                self._endpoint, self._resource
            )
        name, id_ = await cmn.name_and_id(self._endpoint, self._resource)
        self.name = name
        self.id = id_

        data = await cmn.get_by_resource(self._endpoint, self._resource)
        self._safe_update(data)
        self._loaded = True

    @classmethod
    async def get_resource(cls, endpoint: str, resource: Resource,
                           **kwargs) -> Type['PokeAPIResource']:
        """Async wrapper function for creating a new APIResource instance."""
        apiresource = cls(endpoint, resource, **kwargs)
        await apiresource._load()
        return apiresource


class APIMetaData(PokeAPIBase):
    """Simple class used for sub-dicts and -lists in a response JSON."""

    @staticmethod
    def _from_data(key: str, data: Union[dict, list]
                   ) -> Union['APIMetaData', List['APIMetaData']]:
        if isinstance(data, dict):
            return APIMetaData(key, data)
        elif isinstance(data, list) \
                and all(isinstance(entry, dict) for entry in data):
            return [APIMetaData(key, entry) for entry in data]
        else:
            raise TypeError(
                'APIMetaData can only be created from a dict or list of dicts.'
            )

    def __init__(self, key: str, data: dict) -> None:
        self._key = key
        self._safe_update(data)

    def __str__(self) -> str:
        return self._key

    def __repr__(self) -> str:
        return f'<APIMetaData object for key "{self._key}">'

    async def as_resource(self, raise_error: bool = False,
                          **kwargs) -> PokeAPIResource:
        """Creates a new APIResource based on the URL from this class."""
        if getattr(self, 'url', False):
            endpoint, resource = cmn.break_url(self.url)
            return await PokeAPIResource.get_resource(
                endpoint, resource, **kwargs)
        elif raise_error:
            raise AttributeError(
                f'object {repr(self)} has no attribute "url" and thus cannot'
                'be loaded as a resource'
            )
        else:
            return None


def make_object(key: str, obj: Any) -> Any:
    """Turns a dict or list of dicts into an APIMetaData object or a list of
    APIMetaData objects and does nothing otherwise.
    """
    if isinstance(obj, (dict, list)):
        return APIMetaData._from_data(key, obj)
    return obj


async def get_subresource(name: str, url: str
                          ) -> Union[APIMetaData, List[APIMetaData]]:
    """Async wrapper function for creating a new APIMetaData instance."""
    data = await cmn.get_by_url(url)
    apimetadata = APIMetaData._from_data(name, data)
    return apimetadata

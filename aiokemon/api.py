import asyncio
from typing import Any, Optional

import aiokemon.common as cmn
import aiokemon.resourcematcher as matcher
from aiokemon.common import Resource

FIND_MATCH = True


class APIResource:
    """Forward declaration of APIResource for type hinting purposes."""


class APIResource:
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
        only be guaranteed once the async function _load is called.
        """
        if custom is not None:
            cmn.set_safe_attrs(self, **custom)
        self._endpoint = endpoint
        self._resource = resource
        self._loaded = False

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<{self._endpoint}-{self._resource}>'

    async def _load(self) -> APIResource:
        """Asynchronously loads the information for the given resource
        in-place and returns a reference to itself.
        """
        if FIND_MATCH and isinstance(self._resource, str):
            self._resource = await matcher.best_match(
                self._endpoint, self._resource
            )
        name, id_ = await cmn.name_and_id(self._endpoint, self._resource)
        self.name = name
        self.id = id_

        data = await cmn.get_by_resource(self._endpoint, self._resource)
        sanitized_data = sanitize_data(data)

        cmn.set_safe_attrs(self, **sanitized_data)
        self._loaded = True


class APIMetaData:
    """More simple class for when data doesn't need to be loaded."""

    def __init__(self, data: dict) -> None:
        sanitized_data = sanitize_data(data)
        cmn.set_safe_attrs(self, **sanitized_data)

    async def as_resource(self) -> APIResource:
        """Creates a new APIResource based on the URL from this class."""
        if getattr(self, 'url', False):
            endpoint, resource = cmn.break_url(self.url)
            print(endpoint, resource)
            return await get_resource(endpoint, resource)
        else:
            return None


def make_object(obj: Any) -> Any:
    """Turns a dictionary into an APIMetaData object and does nothing
    otherwise.
    """
    if isinstance(obj, dict):
        return APIMetaData(obj)
    return obj


def sanitize_data(data: dict) -> dict:
    """Sanitizes a data dictionary so all of its keys can be added as
    attributes to a class. Also converts any sub-dictionaries into
    classes.
    """
    sanitized_data = {}

    for k, v in data.items():
        sanitized_key = cmn.sanitize_attribute(k)
        if isinstance(v, dict):
            sanitized_data[sanitized_key] = make_object(v)
        elif isinstance(v, list):
            sanitized_data[sanitized_key] = [make_object(v_) for v_ in v]
        else:
            sanitized_data[sanitized_key] = v

    return sanitized_data


async def get_resource(endpoint: str, resource: Resource,
                       **kwargs) -> APIResource:
    """Async wrapper function for creating a new resource class."""
    apiresource = APIResource(endpoint, resource, **kwargs)
    await apiresource._load()
    return apiresource


async def test():
    print('Doing test()...')
    p = await get_resource('pokemon', 'breloom')
    print(p.name)
    print(p.abilities[0].ability.name)
    ability = await p.abilities[0].ability.as_resource()
    print(ability.name)
    print(dir(ability))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())

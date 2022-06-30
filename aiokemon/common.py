import keyword
from typing import Optional, Tuple, Union

import aiohttp
import requests

BASE_URL = 'https://pokeapi.co/api/v2'
VALID_ENDPOINTS = set(requests.get(BASE_URL).json())
Resource = Union[str, int]


def join_url(*url_components: str) -> str:
    """Returns a URL by stripping the components of trailing forward slashes
    and then joining them with forward slashes.
    """
    return '/'.join(component.strip('/') for component in url_components)


def break_url(url: str) -> Tuple[str, str]:
    """Breaks apart a URL into the endpoint and resource."""
    index = url.find(BASE_URL)
    if index == -1:
        raise ValueError(f'base URL "{BASE_URL}" is not in that URL.')
    url_component = url[index + len(BASE_URL):].strip('/').split('/')
    endpoint, resource = url_component
    try:
        return endpoint, int(resource)
    except ValueError:
        return endpoint, resource


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


def set_safe_attrs(self_: object, **attr_value_pairs) -> None:
    for k, v in attr_value_pairs.items():
        setattr(self_, sanitize_attribute(k), v)


async def get_json(url: str) -> dict:
    """Asynchronously gets a json as a dictionary from a GET request.

    ## Raises
    `aiohttp.ClientResponseError` if there was an error during the request.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()


async def get_by_resource(endpoint: str, resource: Optional[Resource] = None,
                          querystring: Optional[str] = None) -> dict:
    """Joins the base URL, the endpoint, the resource, and the querystring
    together, then asynchronously sends a GET request for it.
    """
    if resource is not None and querystring is not None:
        raise ValueError(
            "resource OR querystring can be non-None, but not both."
        )
    url = join_url(BASE_URL, endpoint)
    if resource is not None:
        url += '/' + str(resource).lstrip('/')
    if querystring is not None:
        url += '?' + querystring.lstrip('?')
    json_data = await get_json(url)
    json_data['url'] = url
    return json_data


async def name_and_id(endpoint: str, resource: Resource) -> Tuple[str, int]:
    """Returns the name and ID of a given resource."""
    if isinstance(resource, str):
        res = await get_by_resource(endpoint, resource)
        name = resource
        id_ = res['id']
    elif isinstance(resource, int):
        res = await get_by_resource(endpoint, resource)
        name = res['name']
        id_ = resource
    else:
        raise TypeError(
            f'resource must be str or int, not {type(resource)}. '
            f'Value is {repr(resource)}.'
        )

    return name, id_

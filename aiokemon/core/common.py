import keyword
import re
from typing import Optional, Tuple, Union
from urllib.parse import urlparse

import aiohttp_client_cache as aiohttp

import aiokemon.utils.file as fmanager

BASE_URL = 'https://pokeapi.co/api/v2'
VALID_ENDPOINTS = {
    'ability',
    'berry',
    'berry-firmness',
    'berry-flavor',
    'characteristic',
    'contest-effect',
    'contest-type',
    'egg-group',
    'encounter-condition',
    'encounter-condition-value',
    'encounter-method',
    'evolution-chain',
    'evolution-trigger',
    'gender',
    'generation',
    'growth-rate',
    'item',
    'item-attribute',
    'item-category',
    'item-fling-effect',
    'item-pocket',
    'language',
    'location',
    'location-area',
    'machine',
    'move',
    'move-ailment',
    'move-battle-style',
    'move-category',
    'move-damage-class',
    'move-learn-method',
    'move-target',
    'nature',
    'pal-park-area',
    'pokeathlon-stat',
    'pokedex',
    'pokemon',
    'pokemon-color',
    'pokemon-form',
    'pokemon-habitat',
    'pokemon-shape',
    'pokemon-species',
    'region',
    'stat',
    'super-contest-effect',
    'type',
    'version',
    'version-group'
}
Resource = Union[str, int]
backslashes = re.compile(r'/+')
cache = aiohttp.SQLiteBackend(
    cache_name=fmanager.cache_file('aiohttp-requests.db'),
    expire_after=60*60*24*7  # a week (in seconds)
)
loaded_endpoints = {}


def join_url(*url_parts: str, query: Optional[str] = None) -> str:
    """Returns a URL by stripping the components of trailing forward slashes
    and then joining them with forward slashes. Ignores falsy parts.
    """
    url = '/'.join(part.strip('/') for part in url_parts if part)
    if query:
        url += '?' + query.lstrip('?')
    return url


def break_url(url: str) -> Tuple[str, Union[str, None]]:
    """Breaks apart a URL into the endpoint and resource."""
    if BASE_URL not in url:
        raise ValueError(f'URL must be for PokéAPI. Got "{url}" instead.')
    url_path = urlparse(url).path.strip('/')
    path_components = backslashes.split(url_path)
    endpoint = path_components[2]
    try:
        resource = path_components[3]
        return endpoint, int(resource)
    except ValueError:
        return endpoint, resource
    except IndexError:
        return endpoint, None


def get_resource_id(url: str) -> int:
    """Returns the ID of a resource."""
    return int(url.strip('/').split('/')[-1])


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

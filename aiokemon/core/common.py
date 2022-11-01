import re
from typing import Optional, Tuple, Union
from urllib.parse import urlparse

BASE_URL = 'https://pokeapi.co/api/v2/'
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


def join_url(*url_parts: str, querystring: Optional[str] = None) -> str:
    """Returns a URL by stripping the components of trailing forward slashes
    and then joining them with forward slashes. Ignores falsy parts.
    """
    url = BASE_URL + '/'.join(part.strip('/') for part in url_parts if part)
    if querystring:
        url += '?' + querystring.lstrip('?')
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

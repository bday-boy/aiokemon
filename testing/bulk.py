import asyncio
from timeit import default_timer as timer

import aiohttp
import requests

import aiokemon as ak

BASE_URL = 'https://pokeapi.co/api/v2'
ENDPOINTS = [
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
]


def join_url(*url_parts: str, query = None) -> str:
    """Returns a URL by stripping the components of trailing forward slashes
    and then joining them with forward slashes. Ignores falsy parts.
    """
    url = '/'.join(part.strip('/') for part in url_parts if part)
    if query:
        url += '?' + query.lstrip('?')
    return url


async def get_json(url: str) -> dict:
    """Asynchronously gets a json as a dictionary from a GET request.

    ## Raises
    `aiohttp.ClientResponseError` if there was an error during the request.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()


async def get_all_resources(endpoint: str) -> dict:
    """Queries an endpoint for all of its resources."""
    url = join_url(BASE_URL, endpoint, query='limit=100000')
    return await get_json(url)


async def all_pokemon_async():
    pokemon_results = (await get_all_resources('pokemon')).get('results')
    pokemon_responses = []
    start = timer()
    mons = await asyncio.gather(*(ak.pokemon(mon['name']) for mon in pokemon_results))
    print(f'aiohttp version took {timer() - start} seconds.')
    

async def all_pokemon_sync():
    all_pokemon = (await get_all_resources('pokemon')).get('results')
    pokemon_responses = []
    start = timer()
    for pokemon_entry in all_pokemon:
        pokemon_responses.append(requests.get(pokemon_entry['url']))
    print(f'requests version took {timer() - start} seconds.')


if __name__ == '__main__':
    asyncio.run(all_pokemon_async())
    asyncio.run(all_pokemon_sync())

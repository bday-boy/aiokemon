from typing import Optional, Union

from aiohttp_client_cache import CachedSession, SQLiteBackend, CacheBackend

import aiokemon.core.common as cmn
import aiokemon.utils.file as fmanager
from aiokemon.core.api import PokeAPIResource
from aiokemon.core.common import Resource
from aiokemon.core.loaders import PokeAPIEndpointLoader
from aiokemon.endpoints import *

Resource = Union[str, int]


class PokeAPISession(CachedSession):
    """Session manager for PokéAPI. Pokeapi.co requires the use of a cache, so
    aiohttp_client_cache is used.
    """
    loaded_endpoints = {}

    def __init__(self, *, cache: CacheBackend = None, **kwargs):
        """If no cache is given, an SQLite one is created by default at
        $HOME/.cache/aiohttp-requests.db.
        """
        if not cache:
            cache = SQLiteBackend(
                cache_name=fmanager.cache_file('aiohttp-requests.db'),
                expire_after=60*60*24*7  # a week (in seconds)
            )
        super().__init__(cache=cache, **kwargs)
        self.endpoints = PokeAPIEndpointLoader(self)

    async def get_json(self, url: str) -> dict:
        """Asynchronously gets a json as a dictionary from a GET request. This
        is the only function in this class that actually sends data to/from
        a server.

        ## Raises
        `aiohttp.ClientResponseError` if there was an error during the request.
        """
        async with self.get(url) as response:
            response.raise_for_status()
            json_data = await response.json()
            if isinstance(json_data, dict):
                json_data['url'] = url
            return json_data

    async def get_resource(self, endpoint: str,
                           resource: Optional[Resource] = None,
                           querystring: Optional[str] = None
                           ) -> PokeAPIResource:
        """Joins the base URL, the endpoint, the resource, and the querystring
        together, then asynchronously sends a GET request for it.

        ## Raises
        `ValueError` if:
        - The endpoint or resource is invalid
        - Both the resource and querystring have a value (only one should)
        """
        if resource and querystring:
            raise ValueError(
                "resource OR querystring can have a value, but not both."
            )
        self.validate_endpoint(endpoint)
        if isinstance(resource, int):
            await self.validate_id(endpoint, resource)
        url = cmn.join_url(
            cmn.BASE_URL, endpoint, str(resource or ''), query=querystring
        )
        pokeapi_data = await self.get_json(url)
        return PokeAPIResource(pokeapi_data)

    async def get_all_resources(self, endpoint: str) -> dict:
        """Queries an endpoint for all of its resources."""
        url = cmn.join_url(cmn.BASE_URL, endpoint, query='limit=100000')
        return await self.get_json(url)

    async def load_endpoint(self, endpoint: str):
        """If an endpoint doesn't exist in the endpoint_resources dict, it is
        loaded (if it is a valid endpoint).

        ## Raises
        `ValueError` if the endpoint is not valid.
        """
        if endpoint in PokeAPISession.loaded_endpoints:
            return
        results = (await self.get_all_resources(endpoint)).get('results', [])
        resource_names = {result['name'] for result in results}
        resource_ids = {
            cmn.get_resource_id(result['url']) for result in results
        }
        PokeAPISession.loaded_endpoints[endpoint] = {
            'names': resource_names,
            'ids': resource_ids
        }

    def validate_endpoint(self, endpoint: str) -> None:
        """Validates a given endpoint and resource.

        ## Raises
        `ValueError` if the endpoint is invalid.
        """
        if endpoint not in cmn.VALID_ENDPOINTS:
            raise ValueError(f'endpoint "{endpoint}" does not exist.')

    async def validate_id(self, endpoint: str, id_: int) -> None:
        """Validates a given resource's ID.

        ## Raises
        `ValueError` if the ID is invalid.
        """
        self.validate_endpoint(endpoint)
        await self.load_endpoint(endpoint)
        if id_ not in PokeAPISession.loaded_endpoints[endpoint]['ids']:
            raise ValueError(f'endpoint has no ID "{id_}"')
    
    async def __aenter__(self) -> 'PokeAPISession':
        """Just exists for type hinting."""
        return await super().__aenter__()


async def test():
    import asyncio
    async with PokeAPISession() as session:
        mons = await session.get_all_resources('pokemon')
        breloom = await session.endpoints.pokemon('breloom')
        mega_punch = await session.endpoints.move('mega-punch')
        mon_coros = tuple(session.endpoints.pokemon(res['name'])
                          for res in mons['results']
                          if res['name'].startswith('a'))
        all_res = await asyncio.gather(*mon_coros)
        b = 0


if __name__ == '__main__':
    import asyncio
    asyncio.run(test())

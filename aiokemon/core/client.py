from typing import Optional, Union

from aiohttp_client_cache import CachedSession, SQLiteBackend, CacheBackend

import aiokemon.core.common as cmn
import aiokemon.utils.file as fmanager
from aiokemon.core.api import PokeAPIResource
from aiokemon.core.common import Resource
from aiokemon.core.loaders import PokeAPIEndpointLoader
from aiokemon.core.matcher import ResourceMatcher
from aiokemon.endpoints import *

Resource = Union[str, int]


class PokeAPISession(CachedSession):
    """Session manager for PokéAPI. Pokeapi.co requires the use of a cache, so
    aiohttp_client_cache is used.
    """
    loaded_endpoints = {}

    def __init__(self, *, cache: CacheBackend = None, match: bool = True,
                 **kwargs):
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
        self.matcher = ResourceMatcher() if match else None

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
        if self.matcher is not None and resource and isinstance(resource, str):
            resource = await self.matcher.best_match(endpoint, resource, self)
        url = cmn.join_url(
            cmn.BASE_URL, endpoint, str(resource or ''), query=querystring
        )
        pokeapi_data = await self.get_json(url)
        return PokeAPIResource(endpoint, pokeapi_data)

    async def get_all_resources(self, endpoint: str) -> dict:
        """Queries an endpoint for all of its resources."""
        url = cmn.join_url(cmn.BASE_URL, endpoint, query='limit=100000')
        return await self.get_json(url)

    async def __aenter__(self) -> 'PokeAPISession':
        """Just exists for type hinting."""
        return await super().__aenter__()


if __name__ == '__main__':
    import asyncio

    async def test_session():
        async with PokeAPISession() as session:
            mons = await session.get_all_resources('pokemon')
            breloom = await session.endpoints.pokemon('breloom')
            mega_punch = await session.endpoints.move('mega-punch')
            mon_coros = tuple(session.endpoints.pokemon(res['name'])
                              for res in mons['results'])[:20]
            all_res = await asyncio.gather(*mon_coros)
            b = 0

    async def test_matcher():
        async with PokeAPISession() as session:
            breloom = await session.endpoints.pokemon('brelom')
            b = 0

    asyncio.run(test_session())

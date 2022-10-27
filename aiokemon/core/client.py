from typing import Optional, Union

from aiohttp.typedefs import StrOrURL
from aiohttp import ClientSession
from aiohttp_client_cache import CachedSession, SQLiteBackend, CacheBackend

import aiokemon.core.common as cmn
import aiokemon.utils.file as fmanager

Resource = Union[str, int]


class PokeAPISession(CachedSession):
    """Session manager for PokeAPI."""
    loaded_endpoints = {}

    def __init__(self, *, cache: CacheBackend = None, **kwargs):
        if not cache:
            cache = SQLiteBackend(
                cache_name=fmanager.cache_file('aiohttp-requests.db'),
                expire_after=60*60*24*7  # a week (in seconds)
            )
        super().__init__(cache=cache, **kwargs)

    async def get_json(self, url: str) -> dict:
        """Asynchronously gets a json as a dictionary from a GET request.

        ## Raises
        `aiohttp.ClientResponseError` if there was an error during the request.
        """
        async with self.get(url) as response:
            response.raise_for_status()
            return await response.json()

    async def get_by_resource(self, endpoint: str,
                              resource: Optional[Resource] = None,
                              querystring: Optional[str] = None) -> dict:
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
        json_data = await self.get_json(url)
        if isinstance(json_data, dict):
            json_data['url'] = url
        return json_data

    async def get_by_url(self, url: str) -> dict:
        """Gets a resource directly via the url. Useful for situations like
        Pokemon encounters, which are a sub-resource.
        """
        json_data = await self.get_json(url)
        if isinstance(json_data, dict):
            json_data['url'] = url
        return json_data

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


async def test():
    async with PokeAPISession() as session:
        mons = await session.get_all_resources('pokemon')
        breloom = await session.get_by_resource('pokemon', 'breloom')
        mega_punch = await session.get_by_resource('move', 'mega-punch')
        print(mons)

    async with ClientSession() as session:
        mon_coros = (
            session.get(res['url']) for res in mons['results']
        )
        all_res = await asyncio.gather(*mon_coros)
        b = 0



if __name__ == '__main__':
    import asyncio
    asyncio.run(test())

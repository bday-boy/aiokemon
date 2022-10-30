from types import TracebackType
from typing import Dict, List, Optional, Type, Union

from aiohttp import ClientSession

import aiokemon.core.common as cmn
from aiokemon.core.cache import cache_get, EmptyCache, JSONCache
from aiokemon.core.matcher import ResourceMatcher


class PokeAPIClientBase:
    def __init__(self, session: Optional[ClientSession] = None, *,
                 match: bool = True, cache=None, should_cache: bool = True
                 ) -> None:
        self._session = session or ClientSession()
        self._matcher = ResourceMatcher() if match else None
        if should_cache:
            self._cache = cache or JSONCache()
        else:
            self._cache = EmptyCache()

    async def close(self) -> None:
        """Ends the session and dumps the cache."""
        if self._session:
            await self._session.close()
        self._cache.safe_dump()

    @cache_get
    async def _get(self, endpoint: str, resource: Optional[str] = None,
                   querystring: Optional[str] = None) -> Union[Dict, List]:
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
        if self._matcher is not None and isinstance(resource, str):
            resource = await self._matcher.best_match(endpoint, resource, self)
        url = cmn.join_url(endpoint, resource, query=querystring)
        json_data = await self._get_json(url)
        if isinstance(json_data, dict):
            json_data['url'] = url
        return json_data

    async def _get_json(self, url: str) -> Union[Dict, List]:
        """Queries the PokeAPI server and returns the JSON response."""
        async with self._session.get(url) as response:
            response.raise_for_status()
            json_data = await response.json()
        return json_data

    async def get_available_resources(self, endpoint: str) -> dict:
        """Queries an endpoint for all its existing resources."""
        url = cmn.join_url(endpoint, query='limit=100000')
        return await self._get_json(url)

    async def __aenter__(self) -> 'PokeAPIClientBase':
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        await self.close()


if __name__ == '__main__':
    import asyncio

    async def test():
        async with PokeAPIClientBase(should_cache=False) as session:
            mons = await session._get('pokemon', querystring='limit=10000')
            mon_coros = tuple(session._get('pokemon', res['name'])
                              for res in mons['results'])
            await asyncio.gather(*mon_coros)

            moves = await session._get('move', querystring='limit=100000')
            move_coros = tuple(session._get('move', res['name'])
                               for res in moves['results'])
            await asyncio.gather(*move_coros)

            a = 0

    async def test_matcher():
        async with PokeAPIClientBase() as session:
            await session._get('pokemon', 'brelom')
            await session._get('pokemon', 'drilfoon')
            await session._get('pokemon', 'vileplume')
            await session._get('pokemon', 'bouldore')
            await session._get('pokemon', 'garchom')
            b = 0

    asyncio.run(test_matcher())

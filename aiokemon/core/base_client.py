from types import TracebackType
from typing import Dict, List, Optional, Type, Union

from aiohttp import ClientSession

import aiokemon.core.common as cmn
from aiokemon.core.cache import JSONCache, cache_get
from aiokemon.core.matcher import ResourceMatcher


class PokeAPIClientBase:
    def __init__(self, session: Optional[ClientSession] = None,
                 match: bool = True, cache=None) -> None:
        self._session = session or ClientSession()
        self._cache = cache or JSONCache()
        self._matcher = ResourceMatcher() if match else None

    async def close(self) -> None:
        """Ends the session and dumps the cache."""
        if self._session:
            await self._session.close()
        self._cache.safe_dump()

    @cache_get
    async def get(self, endpoint: str, resource: Optional[str] = None,
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
        async with PokeAPIClientBase() as session:
            mons = await session.get('pokemon', querystring='limit=10000')
            mon_coros = tuple(session.get('pokemon', res['name'])
                              for res in mons['results'])
            await asyncio.gather(*mon_coros)

            moves = await session.get('move', querystring='limit=100000')
            move_coros = tuple(session.get('move', res['name'])
                               for res in moves['results'])
            await asyncio.gather(*move_coros)

    asyncio.run(test())

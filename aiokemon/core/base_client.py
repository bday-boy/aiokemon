import json
from types import TracebackType
from typing import Dict, List, Optional, Type, Union

from aiohttp import ClientSession

import aiokemon.core.common as cmn
from aiokemon.core.cache import cache_get, EmptyCache, PickleFileCache
from aiokemon.core.matcher import ResourceMatcher


class PokeAPIClientBase:
    def __init__(self, session: Optional[ClientSession] = None, *,
                 match: bool = True, cache=None, should_cache: bool = True
                 ) -> None:
        self._session = session or ClientSession()
        self._matcher = ResourceMatcher() if match else None
        if should_cache:
            self._cache = cache or PickleFileCache()
        else:
            self._cache = EmptyCache()

    async def close(self) -> None:
        """Ends the session and dumps the cache."""
        if self._session:
            await self._session.close()
        self._cache.safe_dump()

    @cache_get
    async def _get_response_text(self, endpoint: str,
                                 resource: Optional[str] = None,
                                 querystring: Optional[str] = None,
                                 url: Optional[str] = None
                                 ) -> str:
        """Queries the PokeAPI server and returns the response text."""
        if url is None:
            url = cmn.join_url(endpoint, resource, querystring=querystring)
        async with self._session.get(url) as response:
            response.raise_for_status()
            response_text = await response.text()
        return response_text

    async def _get_json(self, endpoint: str, resource: Optional[str] = None,
                        querystring: Optional[str] = None
                        ) -> Union[Dict, List]:
        """Joins the base URL, the endpoint, the resource, and the querystring
        together, then asynchronously sends a GET request for it.

        ## Raises
        `ValueError` if:
        - The endpoint is invalid
        - Both the resource and querystring have a value (only one should)
        """
        if resource and querystring:
            raise ValueError(
                "resource OR querystring can have a value, but not both."
            )
        if self._matcher is not None and isinstance(resource, str):
            resource = await self._matcher.best_match(endpoint, resource, self)
        url = cmn.join_url(endpoint, resource, querystring=querystring)
        response_text = await self._get_response_text(endpoint, url=url)
        json_data = json.loads(response_text)
        if isinstance(json_data, dict):
            json_data['url'] = url
        return json_data

    async def get_available_resources(self, endpoint: str) -> dict:
        """Queries an endpoint for all its existing resources."""
        response_text = await self._get_response_text(
            endpoint, querystring='limit=100000'
        )
        return json.loads(response_text)

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
            mons = await session._get_json('pokemon', querystring='limit=10000')
            mon_coros = tuple(session._get_json('pokemon', res['name'])
                              for res in mons['results'])
            await asyncio.gather(*mon_coros)

            moves = await session._get_json('move', querystring='limit=100000')
            move_coros = tuple(session._get_json('move', res['name'])
                               for res in moves['results'])
            await asyncio.gather(*move_coros)

            a = 0

    async def test_matcher():
        async with PokeAPIClientBase() as session:
            await session._get_json('pokemon', 'brelom')
            await session._get_json('pokemon', 'drilfoon')
            await session._get_json('pokemon', 'vileplume')
            await session._get_json('pokemon', 'bouldore')
            await session._get_json('pokemon', 'garchom')
            b = 0

    asyncio.run(test())

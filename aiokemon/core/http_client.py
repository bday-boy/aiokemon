from types import TracebackType
from typing import Dict, List, Optional, Type, Union

from aiohttp import ClientSession

import aiokemon.core.common as cmn
from aiokemon.core.cache import JSONCache, cache_get


class SimpleHTTPCacheClient:
    def __init__(self, session: Optional[ClientSession] = None,
                 cache = None) -> None:
        self._session = session or ClientSession()
        self._cache = cache or JSONCache()

    async def close(self) -> None:
        """Ends the session and dumps the cache."""
        if self._session:
            await self._session.close()
        self._cache.safe_dump()

    @cache_get
    async def get(self, endpoint: str, resource: Optional[str] = None,
                  querystring: Optional[str] = None) -> Union[Dict, List]:
        """Queries the server for a response and returns the JSON."""
        url = cmn.join_url(endpoint, resource, query=querystring)
        async with self._session.get(url) as response:
            response.raise_for_status()
            json_data = await response.json()
        if isinstance(json_data, dict):
            json_data['url'] = url
        return json_data

    async def __aenter__(self) -> 'SimpleHTTPCacheClient':
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
        async with SimpleHTTPCacheClient() as session:
            mons = await session.get('pokemon', querystring='limit=10000')
            mon_coros = tuple(session.get('pokemon', res['name'])
                              for res in mons['results'])
            await asyncio.gather(*mon_coros)

            moves = await session.get('move', querystring='limit=100000')
            move_coros = tuple(session.get('move', res['name'])
                               for res in moves['results'])
            await asyncio.gather(*move_coros)

    asyncio.run(test())

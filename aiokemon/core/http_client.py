from types import TracebackType
from typing import Dict, List, Optional, Type, Union

from aiohttp import ClientSession

from cache import JSONCache

class cmn:
    BASE_URL = ''

    @staticmethod
    def join_url(*url_parts, qs: Optional[str] = None):
        url = '/'.join(part.strip('/') for part in url_parts if part)
        if qs:
            url += '?' + qs.lstrip('?')
        return url


class SimpleHTTPCacheClient:
    def __init__(self, session: Optional[ClientSession] = None,
                 cache = None) -> None:
        self._session = session or ClientSession()
        self._cache = cache or JSONCache()

    async def close(self) -> None:
        """Ends the session and dumps the cache."""
        if self._session:
            await self._session.close()

    async def get(self, endpoint: str, resource: str, querystring: str
                  ) -> Union[Dict, List]:
        """Queries the server for a response and returns the JSON."""
        url = cmn.join_url(cmn.BASE_URL, endpoint, resource, qs=querystring)
        async with self._session.get(url) as response:
            await response.raise_for_status()

            if self._cache.has(endpoint, resource, url):
                return self._cache(endpoint, resource, url)

            json_data = await response.json()
            if isinstance(json_data, dict):
                json_data['url'] = url
            self._cache.put(endpoint, resource, url, json_data)
            return json_data

    async def __aenter__(self):
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
        base_url = 'https://woot.com/'
        test_dict = {
            'jdsiofjsdafd': [
                'fdsifojdsofjds',
                'fdjsiofjdsofjdso',
                15,
                'asdiodjifojds'
            ],
            'fdsjifojdsofjd': 'yeahhheahfduhishif'
        }
        async with SimpleHTTPCacheClient() as session:
            for i, s in enumerate(('test', 'yeehaw', 'yeahbaby')):
                session._cache.put(s, f'{s}{i}', f'{base_url}/{s}/{s}{i}', test_dict)
            raise Exception

    asyncio.run(test())

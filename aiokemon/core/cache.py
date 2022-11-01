import hashlib
import json
import pickle
import zlib
from collections import UserDict
from typing import Dict, List, Optional, Union
from pathlib import Path

import aiokemon.core.common as cmn

JSONSerializable = Union[Dict, List]


def make_key(resource: str, url: str) -> str:
    """Since URLs contain an abundance of characters unsafe for use in
    filenames, the keys used for each endpoint dict are the hashed URL
    appended to the requested resource.
    """
    return f'{resource}{hashlib.md5(bytes(url, "utf-8")).hexdigest()}'


class BaseCache:
    """Base class to be used for user-created caches. Any cache class that
    inherits this class must implement the following methods:

    - `get(self, endpoint: str, resource: str, url: str)`: Gets the cached data.
    - `put(self, endpoint: str, resource: str, url: str,
    data: JSONSerializable)`: Puts the cached data into the cache.
    - `has(endpoint: str, resource: str, url: str)`: Checks if the data exists
    in the cache.
    """

    def get(self, *args, **kwargs) -> Union[JSONSerializable, None]:
        raise NotImplementedError('Cache needs a `get` method to work.')

    def put(self, *args, **kwargs) -> None:
        raise NotImplementedError('Cache needs a `put` method to work.')

    def has(self, *args, **kwargs) -> bool:
        raise NotImplementedError('Cache needs a `has` method to work.')

    def safe_dump(self, *args, **kwargs) -> bool:
        raise NotImplementedError('Cache needs a `safe_dump` method to work.')


class EmptyCache(BaseCache):
    """Cache class used when no caching is desired."""

    def put(self, *args, **kwargs) -> None:
        pass

    def has(self, *args, **kwargs) -> bool:
        return False

    def safe_dump(self, *args, **kwargs) -> bool:
        pass


class PickleLoader(UserDict):
    """Custom dict class created to act like a defaultdict that loads cached
    pickle files when an endpoint is accessed for the first time.
    """

    def __init__(self, cache_dir: Optional[Path] = None, *args,
                 **kwargs) -> None:
        if cache_dir is None:
            self.cache_dir = Path.home() / '.cache' / 'aiokemon'
        elif isinstance(cache_dir, str):
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = cache_dir
        if not self.cache_dir.is_dir():
            self.cache_dir.mkdir(parents=True)
        super().__init__(*args, **kwargs)

    def get_file_path(self, endpoint) -> Path:
        return self.cache_dir / f'{endpoint}.pickle'

    def dump_dict(self, endpoint: str, data: Dict[str, bytes]) -> None:
        file_path = self.get_file_path(endpoint)
        with open(file_path, 'wb') as pickle_file:
            pickle.dump(data, pickle_file)

    def load_dict(self, file_path: Path) -> Dict[str, bytes]:
        with open(file_path, 'rb') as pickle_file:
            pickle_data = pickle_file.read()
            if not pickle_data:
                return {}
            return pickle.loads(pickle_data)

    def __getitem__(self, endpoint: str) -> Dict[str, bytes]:
        if endpoint not in self:
            file_path = self.get_file_path(endpoint)
            if file_path.exists():
                self[endpoint] = self.load_dict(file_path)
            else:
                self[endpoint] = {}
        return super().__getitem__(endpoint)


class PickleFileCache(BaseCache):
    """A simple cache class that uses pickle files to load each endpoint
    cache as they are requested. When an endpoint is requested for the first
    time, the entire endpoint's cache is loaded into memory, so this can get
    quite large quickly.
    """

    def __init__(self, cache_dir: Optional[Path] = None, *args,
                 **kwargs) -> None:
        self._cache_dict = PickleLoader(cache_dir, *args, **kwargs)

    def get(self, endpoint: str, resource: str, url: str
            ) -> Union[Dict, List, None]:
        cached_data = self._cache_dict[endpoint].get(make_key(resource, url))
        if cached_data:
            # Decompress base64 bytes and decode to UTF-8 string
            bin_dict = zlib.decompress(cached_data).decode('utf-8')
            cached_data = json.loads(bin_dict)
        return cached_data

    def put(self, endpoint: str, resource: str, url: str,
            data: JSONSerializable) -> None:
        # Convert JSON str to bytes then compress into bytes
        compressed_data = zlib.compress(bytes(json.dumps(data), 'utf-8'))
        self._cache_dict[endpoint][make_key(resource, url)] = compressed_data

    def has(self, endpoint: str, resource: str, url: str) -> bool:
        return make_key(resource, url) in self._cache_dict[endpoint]

    def safe_dump(self) -> None:
        print('Dumping cache...')
        try:
            self._dump_cache()
        except NameError as e:
            if "name 'open' is not defined" in e.args:
                raise RuntimeError(
                    "Couldn't dump cache at all. Python raised an exception "
                    'before the cache was dumped and the open() function from '
                    "Python's standard library was deleted from the global "
                    'namespace before the cache got a chance to dump into a '
                    'file. To attempt to avoid this problem in the future, '
                    'you can manually dump the cache at any point by calling'
                    'the safe_dump function.'
                )
        print('Cache dumped.')

    def _dump_cache(self) -> None:
        for endpoint in self._cache_dict:
            self._cache_dict.dump_dict(endpoint, self._cache_dict[endpoint])


def cache_get(get_coro):
    async def cache_wrapper(session, endpoint: str,
                            resource: Optional[str] = None,
                            querystring: Optional[str] = None):
        url = cmn.join_url(endpoint, resource, query=querystring)
        if session._cache.has(endpoint, resource, url):
            return session._cache.get(endpoint, resource, url)
        json_data = await get_coro(
            session, endpoint, resource, querystring
        )
        session._cache.put(endpoint, resource, url, json_data)
        return json_data

    return cache_wrapper


if __name__ == '__main__':
    c = PickleFileCache()
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
    for i, s in enumerate(('test', 'yeehaw', 'yeahbaby')):
        c.put(s, f'{s}{i}', f'{base_url}/{s}/{s}{i}', test_dict)
    c.safe_dump()

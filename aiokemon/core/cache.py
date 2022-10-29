import hashlib
import json
from collections import UserDict
from typing import Dict, List, Optional, Union
from pathlib import Path

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


class JSONLoader(UserDict):
    """Custom dict class created to act like a defaultdict that loads cached
    JSON files when an endpoint is accessed for the first time.
    """

    def __init__(self, cache_dir: Optional[Path] = None, *args,
                 **kwargs) -> None:
        if cache_dir is None:
            self.cache_dir = Path.home() / '.cache' / 'pokeapi_json_cache'
        elif isinstance(cache_dir, str):
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = cache_dir
        if not self.cache_dir.is_dir():
            self.cache_dir.mkdir(parents=True)
        super().__init__(*args, **kwargs)

    def get_json_path(self, endpoint) -> Path:
        return self.cache_dir / f'{endpoint}.json'

    def __getitem__(self, endpoint: str) -> JSONSerializable:
        if endpoint not in self:
            json_path = self.get_json_path(endpoint)
            if json_path.exists():
                with open(json_path) as json_file:
                    cached_data = json.load(json_file)
                    self[endpoint] = cached_data
            else:
                self[endpoint] = {}
        return super().__getitem__(endpoint)


class JSONCache(BaseCache):
    """A simple cache class that uses JSON files to load each endpoint
    cache as they are requested. When an endpoint is requested for the first
    time, the entire endpoint's cache is loaded into memory, so this can get
    quite large quickly.
    """

    def __init__(self, cache_dir: Optional[Path] = None, *args,
                 **kwargs) -> None:
        self._cache_dict = JSONLoader(cache_dir, *args, **kwargs)

    def get(self, endpoint: str, resource: str, url: str
            ) -> Union[Dict, List, None]:
        return self._cache_dict[endpoint].get(make_key(resource, url))

    def put(self, endpoint: str, resource: str, url: str,
            data: JSONSerializable) -> None:
        self._cache_dict[endpoint][make_key(resource, url)] = data

    def has(self, endpoint: str, resource: str, url: str) -> bool:
        return make_key(resource, url) in self._cache_dict[endpoint]

    def safe_dump(self) -> None:
        try:
            self._dump_cache()
        except (FileNotFoundError, TypeError, ValueError):
            import pickle
            print(
                'Something went wrong when dumping the cache jsons. '
                'Dumping the entire JSONLoader object as a pickle file '
                'in the current directory instead.'
            )
            with open('emergency_cache_dump.pkl', 'w') as f:
                pickle.dump(self._cache_dict, f)
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
        print('Dumping cache...')

    def _dump_cache(self) -> None:
        for endpoint in self._cache_dict:
            json_path = self._cache_dict.get_json_path(endpoint)
            with open(json_path, 'w') as json_file:
                json.dump(self._cache_dict[endpoint], json_file, indent=2)


if __name__ == '__main__':
    c = JSONCache()
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

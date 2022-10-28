import json
from typing import Optional, Union
from pathlib import Path

import aiofiles

import aiokemon.core.common as cmn
from aiokemon.core.common import Resource
from aiokemon.utils.file import make_cache

cache_dict = {}
cache_dir = make_cache() / 'pokeapi_json_cache'
cache_dir.mkdir()

def cache(endpoint: str) -> None:
    async def cache_wrapper(session, resource: Resource) -> dict:
        pass
    return cache_wrapper


class JSONCache:
    def __init__(self, cache_dir: Optional[Union[Path, str]] = None) -> None:
        if cache_dir is None:
            self.cache_dir = make_cache() / 'pokeapi_json_cache'
        elif isinstance(cache_dir, str):
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = cache_dir
        self.cache_dir.mkdir()

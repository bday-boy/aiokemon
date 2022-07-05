import os
from typing import Optional

home = os.path.expanduser('~')


def make_cache() -> str:
    """Creates a .cache directory at the user's home if one doesn't
    already exist.

    ## Raises
    `OSError` if the .cache directory couldn't be made.
    """
    cache_dir = os.path.join(home, '.cache')
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)
        if not os.path.isdir(cache_dir):
            raise OSError(
                "couldn't create the .cache directory. Please create one "
                "manually in your user's home directory."
            )
    return cache_dir


def cache_file(cache_file: str, *, cache_dir: Optional[str] = None) -> str:
    """Gets the path to a cache file of the given name. If a .cache directory
    doesn't exist in the user's home and no cache_dir is passed, one is
    created.
    """
    if cache_dir is None:
        cache_dir = make_cache()
    return os.path.join(cache_dir, cache_file)

from pathlib import Path
from typing import Optional, Union

home = Path('~').expanduser()


def make_cache() -> Union[str, Path]:
    """Creates a .cache directory at the user's home if one doesn't
    already exist.

    ## Raises
    `OSError` if the .cache directory couldn't be made.
    """
    cache_dir = home / '.cache'
    if not cache_dir.is_dir():
        cache_dir.mkdir()
        if not cache_dir.is_dir():
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
    return str(cache_dir / cache_file)

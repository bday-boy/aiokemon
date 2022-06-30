import os

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
                "manually at ~/.cache"
            )
    return cache_dir


def cache_file(cache_file: str) -> str:
    cache_dir = make_cache()
    return os.path.join(cache_dir, cache_file)

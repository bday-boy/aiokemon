import re
from typing import Tuple

import aiokemon.core.common as cmn
from aiokemon.utils.text import levenshtein_osa

and_pokemon = re.compile(r'\s?(pok[eé]mon|and)\s?', re.IGNORECASE)
non_alphanumerical = re.compile(r'[^a-z0-9]', re.IGNORECASE)


def get_searches(endpoint: str, resource_attempt: str) -> Tuple[str, str]:
    """Formats searches to fit the syntax of the endpoints.

    TODO: Add custom formatter for certain endpoints, like one for game
    to remove 'and'.
    """
    if endpoint in {'version', 'version-group'}:
        resource_attempt = and_pokemon.sub(' ', resource_attempt).strip()
    split_resource = non_alphanumerical.split(resource_attempt)
    return (
        '-'.join(split_resource), '-'.join(reversed(split_resource))
    )


def add_matches(endpoint: str, search: str, matches: list) -> None:
    """Computes string distance between the search and the actual endpoint
    for each resource in the endpoint and adds it to the matches list.
    """
    for resource in cmn.endpoints[endpoint]['names']:
        matches.append((resource, levenshtein_osa(resource, search)))


async def best_match(endpoint: str, resource_attempt: str) -> str:
    """Finds the best match for a given resource of a given endpoint."""
    await cmn.validate_endpoint(endpoint)
    await cmn.load_endpoint_resources(endpoint)

    # Don't need to bother searching if it's an exact match
    if resource_attempt in cmn.endpoints[endpoint]['names']:
        return resource_attempt

    matches = []
    search_1, search_2 = get_searches(endpoint, resource_attempt)

    add_matches(endpoint, search_1, matches)
    if search_1 != search_2:
        add_matches(endpoint, search_2, matches)

    matches.sort(key=lambda t: t[1])
    return matches[0][0]

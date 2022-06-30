import re
from typing import Tuple

import aiokemon.common as cmn

non_alphanumerical = re.compile(r'[^a-z0-9]', re.IGNORECASE)
endpoint_resources = {}


def _get_searches(resource_attempt: str) -> Tuple[str, str]:
    """Formats searches to fit the syntax of the endpoints.

    TODO: Add custom formatter for certain endpoints, like one for game
    to remove 'and'.
    """
    split_resource = non_alphanumerical.split(resource_attempt)
    return (
        '-'.join(split_resource), '-'.join(reversed(split_resource))
    )

async def _get_all_resources(endpoint: str) -> dict:
    """Queries an endpoint for all of its resources."""
    return await cmn.get_by_resource(endpoint, querystring='limit=100000')

async def _load_endpoint(endpoint: str):
    """If an endpoint doesn't exist in the endpoint_resources dict, it is
    loaded (if it is a valid endpoint).

    ## Raises
    `ValueError` if the endpoint is not valid.
    """
    if endpoint not in cmn.VALID_ENDPOINTS:
        raise ValueError(f'{endpoint} is not a valid endpoint.')
    resources = await _get_all_resources(endpoint)
    valid_resources = {result['name'] for result in resources['results']}
    endpoint_resources[endpoint] = valid_resources

def _add_matches(endpoint: str, search: str, matches: list) -> None:
    """Computes string distance between the search and the actual endpoint
    for each resource in the endpoint and adds it to the matches list.
    """
    for resource in endpoint_resources[endpoint]:
        matches.append((resource, levenshtein_osa(resource, search)))

async def best_match(endpoint: str, resource_attempt: str) -> str:
    """Finds the best match for a given resource of a given endpoint."""
    if endpoint not in endpoint_resources:
        await _load_endpoint(endpoint)

    # Don't need to bother searching if it's an exact match
    if resource_attempt in endpoint_resources[endpoint]:
        return resource_attempt

    matches = []
    search_1, search_2 = _get_searches(resource_attempt)

    _add_matches(endpoint, search_1, matches)
    if search_1 != search_2:
        _add_matches(endpoint, search_2, matches)

    matches.sort(key=lambda t: t[1])
    return matches[0][0]


async def main():
    mon = input('Input something to match: ')
    match = await best_match('pokemon', mon)
    print(f'Best match: {match}')


def levenshtein_osa(a: str, b: str) -> int:
    """A slightly-modified version of the traditional Levenshtein algorithm
    that considers an adjacent character swap as one operation rather than
    two.
    """
    a_len = len(a)
    b_len = len(b)
    D = [[0] * (b_len + 1) for i in range(a_len + 1)]

    for i in range(a_len + 1):
        D[i][0] = i
    for j in range(b_len + 1):
        D[0][j] = j

    for i in range(1, a_len + 1):
        for j in range(1, b_len + 1):
            cost = (a[i - 1] != b[j - 1])
            D[i][j] = min(D[i - 1][j] + 1,          # deletion
                          D[i][j - 1] + 1,          # insertion
                          D[i - 1][j - 1] + cost)   # substitution
            if (i > 1 and j > 1) and (a[i - 1] == b[j - 2]
                                      and a[i - 2] == b[j - 1]):
                D[i][j] = min(
                    D[i][j], D[i - 2][j - 2] + 1    # adjacent transposition
                )

    return D[-1][-1], D[a_len][b_len]


if __name__ == '__main__':
    levenshtein_osa('test', 'testing')

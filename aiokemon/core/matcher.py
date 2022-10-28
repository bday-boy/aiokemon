import re
from typing import Tuple

import aiokemon.core.common as cmn
from aiokemon.utils.text import levenshtein_osa

and_pokemon = re.compile(r'\s?(pok[eé]mon|and)\s?', re.IGNORECASE)
non_alphanumerical = re.compile(r'[^a-z0-9]', re.IGNORECASE)


class ResourceMatcher:
    """Uses fuzzy string matching to find the closest-matching resource
    when the given one doesn't exist.
    """

    def __init__(self) -> None:
        self.cache = {}
        self.loaded_endpoints = {}

    async def _load_endpoint(self, endpoint: str, session):
        """If an endpoint doesn't exist in the endpoint_resources dict, it is
        loaded (if it is a valid endpoint).

        ## Raises
        `ValueError` if the endpoint is not valid.
        """
        results = await session.get_all_resources(endpoint)
        resource_names = {res['name'] for res in results.get('results', [])}
        self.loaded_endpoints[endpoint] = resource_names

    def _validate_endpoint(self, endpoint: str) -> None:
        """Validates a given endpoint and resource.

        ## Raises
        `ValueError` if the endpoint is invalid.
        """
        if endpoint not in cmn.VALID_ENDPOINTS:
            raise ValueError(f'endpoint "{endpoint}" does not exist.')

    def _get_searches(self, endpoint: str, resource_attempt: str) -> Tuple[str, str]:
        """Formats searches to fit the syntax of the endpoints.

        TODO: Add custom formatter for certain endpoints, like one for game
        to remove 'and'.
        """
        if endpoint in {'version', 'version-group'}:
            resource_attempt = and_pokemon.sub(' ', resource_attempt).strip()
        split_resource = non_alphanumerical.split(resource_attempt)
        return '-'.join(split_resource), '-'.join(reversed(split_resource))

    def _add_matches(self, endpoint: str, search: str, matches: list) -> None:
        """Computes string distance between the search and the actual endpoint
        for each resource in the endpoint and adds it to the matches list.
        """
        for resource in self.loaded_endpoints[endpoint]:
            matches.append((resource, levenshtein_osa(resource, search)))

    async def best_match(self, endpoint: str, resource: str, session) -> str:
        """Finds the best match for a given resource of a given endpoint."""
        self._validate_endpoint(endpoint)
        if endpoint not in self.loaded_endpoints:
            await self._load_endpoint(endpoint, session)

        # Don't need to bother searching if it's an exact match
        if resource in self.loaded_endpoints[endpoint]:
            return resource

        matches = []
        search, search_reversed = self._get_searches(endpoint, resource)
        self._add_matches(endpoint, search, matches)

        # Many alt forms in PokeAPI are listed as [alt]-[name] rather than
        # [name]-[alt], i.e. shield-aegislash. So if our search is not the same
        # forwards and backwards, we'll also test the reversed search
        if search != search_reversed:
            self._add_matches(endpoint, search_reversed, matches)

        matches.sort(key=lambda t: t[1])
        return matches[0][0]

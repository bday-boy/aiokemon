from typing import Optional, Union

from aiohttp_client_cache import CachedSession, SQLiteBackend, CacheBackend

import aiokemon.core.common as cmn
import aiokemon.utils.file as fmanager
from aiokemon.core.api import new_pokeapimetadata, PokeAPIResource
from aiokemon.core.common import Resource
from aiokemon.endpoints import *

Resource = Union[str, int]


class PokeAPISessionBase(CachedSession):
    """Session manager for PokéAPI. Pokeapi.co requires the use of a cache, so
    aiohttp_client_cache is used.
    """
    loaded_endpoints = {}

    def __init__(self, *, cache: CacheBackend = None, **kwargs):
        """If no cache is given, an SQLite one is created by default at
        $HOME/.cache/aiohttp-requests.db.
        """
        if not cache:
            cache = SQLiteBackend(
                cache_name=fmanager.cache_file('aiohttp-requests.db'),
                expire_after=60*60*24*7  # a week (in seconds)
            )
        super().__init__(cache=cache, **kwargs)

    async def get_json(self, url: str) -> dict:
        """Asynchronously gets a json as a dictionary from a GET request. This
        is the only function in this class that actually sends data to/from
        a server.

        ## Raises
        `aiohttp.ClientResponseError` if there was an error during the request.
        """
        async with self.get(url) as response:
            response.raise_for_status()
            json_data = await response.json()
            if isinstance(json_data, dict):
                json_data['url'] = url
            return json_data

    async def get_resource(self, endpoint: str,
                           resource: Optional[Resource] = None,
                           querystring: Optional[str] = None
                           ) -> PokeAPIResource:
        """Joins the base URL, the endpoint, the resource, and the querystring
        together, then asynchronously sends a GET request for it.

        ## Raises
        `ValueError` if:
        - The endpoint or resource is invalid
        - Both the resource and querystring have a value (only one should)
        """
        if resource and querystring:
            raise ValueError(
                "resource OR querystring can have a value, but not both."
            )
        self.validate_endpoint(endpoint)
        if isinstance(resource, int):
            await self.validate_id(endpoint, resource)
        url = cmn.join_url(
            cmn.BASE_URL, endpoint, str(resource or ''), query=querystring
        )
        pokeapi_data = await self.get_json(url)
        return PokeAPIResource(pokeapi_data)

    async def get_all_resources(self, endpoint: str) -> dict:
        """Queries an endpoint for all of its resources."""
        url = cmn.join_url(cmn.BASE_URL, endpoint, query='limit=100000')
        return await self.get_json(url)

    async def load_endpoint(self, endpoint: str):
        """If an endpoint doesn't exist in the endpoint_resources dict, it is
        loaded (if it is a valid endpoint).

        ## Raises
        `ValueError` if the endpoint is not valid.
        """
        if endpoint in PokeAPISessionBase.loaded_endpoints:
            return
        results = (await self.get_all_resources(endpoint)).get('results', [])
        resource_names = {result['name'] for result in results}
        resource_ids = {
            cmn.get_resource_id(result['url']) for result in results
        }
        PokeAPISessionBase.loaded_endpoints[endpoint] = {
            'names': resource_names,
            'ids': resource_ids
        }

    def validate_endpoint(self, endpoint: str) -> None:
        """Validates a given endpoint and resource.

        ## Raises
        `ValueError` if the endpoint is invalid.
        """
        if endpoint not in cmn.VALID_ENDPOINTS:
            raise ValueError(f'endpoint "{endpoint}" does not exist.')

    async def validate_id(self, endpoint: str, id_: int) -> None:
        """Validates a given resource's ID.

        ## Raises
        `ValueError` if the ID is invalid.
        """
        self.validate_endpoint(endpoint)
        await self.load_endpoint(endpoint)
        if id_ not in PokeAPISessionBase.loaded_endpoints[endpoint]['ids']:
            raise ValueError(f'endpoint has no ID "{id_}"')


class PokeAPISession(PokeAPISessionBase):
    """The main PokéAPI session handler. Uses a bunch of simple wrapper
    functions to load resources and return type-hinted objects.
    """

    async def berry(self, resource: Resource) -> Berry:
        """Quick berry lookup.

        See https://pokeapi.co/docsv2/#berries for attributes and more detailed
        information.
        """
        return await self.get_resource('berry', resource)

    async def berry_firmness(self, resource: Resource) -> BerryFirmness:
        """Quick berry-firmness lookup.

        See https://pokeapi.co/docsv2/#berry-firmnesses for attributes and more
        detailed information.
        """
        return await self.get_resource('berry-firmness', resource)

    async def berry_flavor(self, resource: Resource) -> BerryFlavor:
        """Quick berry-flavor lookup.

        See https://pokeapi.co/docsv2/#berry-flavors for attributes and more
        detailed information.
        """
        return await self.get_resource('berry-flavor', resource)

    async def contest_type(self, resource: Resource) -> ContestType:
        """Quick contest-type lookup.

        See https://pokeapi.co/docsv2/#contest-types for attributes and more
        detailed information.
        """
        return await self.get_resource('contest-type', resource)

    async def contest_effect(self, id_: int) -> ContestEffect:
        """Quick contest-effect lookup.

        See https://pokeapi.co/docsv2/#contest-effects for attributes and more
        detailed information.
        """
        return await self.get_resource('contest-effect', id_)

    async def super_contest_effect(self, id_: int) -> SuperContestEffect:
        """Quick super-contest-effect lookup.

        See https://pokeapi.co/docsv2/#super-contest-effects for attributes and
        more detailed information.
        """
        return await self.get_resource('super-contest-effect', id_)

    async def encounter_method(self, resource: Resource) -> EncounterMethod:
        """Quick encounter-method lookup.

        See https://pokeapi.co/docsv2/#encounter-methods for attributes and more
        detailed information.
        """
        return await self.get_resource('encounter-method', resource)

    async def encounter_condition(self, resource: Resource, 
                                  ) -> EncounterCondition:
        """Quick encounter-condition lookup.

        See https://pokeapi.co/docsv2/#encounter-conditions for attributes and more
        detailed information.
        """
        return await self.get_resource('encounter-condition', resource)

    async def encounter_condition_value(self, resource: Resource, 
                                        ) -> EncounterConditionValue:
        """Quick encounter-condition-value lookup.

        See https://pokeapi.co/docsv2/#encounter-condition-values for attributes
        and more detailed information.
        """
        return await self.get_resource('encounter-condition-value', resource)

    async def evolution_chain(self, id_: int) -> EvolutionChain:
        """Quick evolution-chain lookup.

        See https://pokeapi.co/docsv2/#evolution-chains for attributes and more
        detailed information.
        """
        return await self.get_resource('evolution-chain', id_)

    async def evolution_trigger(self, resource: Resource) -> EvolutionTrigger:
        """Quick evolution-trigger lookup.

        See https://pokeapi.co/docsv2/#evolution-triggers for attributes and more
        detailed information.
        """
        return await self.get_resource('evolution-trigger', resource)

    async def generation(self, resource: Resource) -> Generation:
        """Quick generation lookup.

        See https://pokeapi.co/docsv2/#generations for attributes and more detailed
        information.
        """
        return await self.get_resource('generation', resource)

    async def pokedex(self, resource: Resource) -> Pokedex:
        """Quick pokedex lookup.

        See https://pokeapi.co/docsv2/#pokedexes for attributes and more detailed
        information.
        """
        return await self.get_resource('pokedex', resource)

    async def version(self, resource: Resource) -> Version:
        """Quick version lookup.

        See https://pokeapi.co/docsv2/#versions for attributes and more detailed
        information.
        """
        return await self.get_resource('version', resource)

    async def version_group(self, resource: Resource) -> VersionGroup:
        """Quick version-group lookup.

        See https://pokeapi.co/docsv2/#version-groups for attributes and more
        detailed information.
        """
        return await self.get_resource('version-group', resource)

    async def item(self, resource: Resource) -> Item:
        """Quick item lookup.

        See https://pokeapi.co/docsv2/#items for attributes and more detailed
        information.
        """
        return await self.get_resource('item', resource)

    async def item_attribute(self, resource: Resource) -> ItemAttribute:
        """Quick item-attribute lookup.

        See https://pokeapi.co/docsv2/#item-attributes for attributes and more
        detailed information.
        """
        return await self.get_resource('item-attribute', resource)

    async def item_category(self, resource: Resource) -> ItemCategory:
        """Quick item-category lookup.

        See https://pokeapi.co/docsv2/#item-categories for attributes and more
        detailed information.
        """
        return await self.get_resource('item-category', resource)

    async def item_fling_effect(self, resource: Resource) -> ItemFlingEffect:
        """Quick item-fling-effect lookup.

        See https://pokeapi.co/docsv2/#item-fling-effects for attributes and more
        detailed information.
        """
        return await self.get_resource('item-fling-effect', resource)

    async def item_pocket(self, resource: Resource) -> ItemPocket:
        """Quick item-pocket lookup.

        See https://pokeapi.co/docsv2/#item-pockets for attributes and more
        detailed information.
        """
        return await self.get_resource('item-pocket', resource)

    async def machine(self, id_: int) -> Machine:
        """Quick machine lookup.

        See https://pokeapi.co/docsv2/#machines for attributes and more detailed
        information.
        """
        return await self.get_resource('machine', id_)

    async def move(self, resource: Resource) -> Move:
        """Quick move lookup.

        See https://pokeapi.co/docsv2/#moves for attributes and more detailed
        information.
        """
        return await self.get_resource('move', resource)

    async def move_ailment(self, resource: Resource) -> MoveAilment:
        """Quick move-ailment lookup.

        See https://pokeapi.co/docsv2/#move-ailments for attributes and more
        detailed information.
        """
        return await self.get_resource('move-ailment', resource)

    async def move_battle_style(self, resource: Resource) -> MoveBattleStyle:
        """Quick move-battle-style lookup.

        See https://pokeapi.co/docsv2/#move-battle-styles for attributes and more
        detailed information.
        """
        return await self.get_resource('move-battle-style', resource)

    async def move_category(self, resource: Resource) -> MoveCategory:
        """Quick move-category lookup.

        See https://pokeapi.co/docsv2/#move-categories for attributes and more
        detailed information.
        """
        return await self.get_resource('move-category', resource)

    async def move_damage_class(self, resource: Resource) -> MoveDamageClass:
        """Quick move-damage-class lookup.

        See https://pokeapi.co/docsv2/#move-damage-classes for attributes and more
        detailed information.
        """
        return await self.get_resource('move-damage-class', resource)

    async def move_learn_method(self, resource: Resource) -> MoveLearnMethod:
        """Quick move-learn-method lookup.

        See https://pokeapi.co/docsv2/#move-learn-methods for attributes and more
        detailed information.
        """
        return await self.get_resource('move-learn-method', resource)

    async def move_target(self, resource: Resource) -> MoveTarget:
        """Quick move-target lookup.

        See https://pokeapi.co/docsv2/#move-targets for attributes and more
        detailed information.
        """
        return await self.get_resource('move-target', resource)

    async def location(self, id_: int) -> Location:
        """Quick location lookup.

        See https://pokeapi.co/docsv2/#locations for attributes and more detailed
        information.
        """
        return await self.get_resource('location', id_)

    async def location_area(self, id_: int) -> LocationArea:
        """Quick location-area lookup.

        See https://pokeapi.co/docsv2/#location-areas for attributes and more
        detailed information.
        """
        return await self.get_resource('location-area', id_)

    async def pal_park_area(self, resource: Resource) -> PalParkArea:
        """Quick pal-park-area lookup.

        See https://pokeapi.co/docsv2/#pal-park-areas for attributes and more
        detailed information.
        """
        return await self.get_resource('pal-park-area', resource)

    async def region(self, resource: Resource) -> Region:
        """Quick region lookup.

        See https://pokeapi.co/docsv2/#regions for attributes and more detailed
        information.
        """
        return await self.get_resource('region', resource)

    async def ability(self, resource: Resource) -> Ability:
        """Quick ability lookup.

        See https://pokeapi.co/docsv2/#abilities for attributes and more detailed
        information.
        """
        return await self.get_resource('ability', resource)

    async def characteristic(self, id_: int) -> Characteristic:
        """Quick characteristic lookup.

        See https://pokeapi.co/docsv2/#characteristics for attributes and more
        detailed information.
        """
        return await self.get_resource('characteristic', id_)

    async def egg_group(self, resource: Resource) -> EggGroup:
        """Quick egg-group lookup.

        See https://pokeapi.co/docsv2/#egg-groups for attributes and more detailed
        information.
        """
        return await self.get_resource('egg-group', resource)

    async def gender(self, resource: Resource) -> Gender:
        """Quick gender lookup.

        See https://pokeapi.co/docsv2/#genders for attributes and more detailed
        information.
        """
        return await self.get_resource('gender', resource)

    async def growth_rate(self, resource: Resource) -> GrowthRate:
        """Quick growth-rate lookup.

        See https://pokeapi.co/docsv2/#growth-rates for attributes and more
        detailed information.
        """
        return await self.get_resource('growth-rate', resource)

    async def nature(self, resource: Resource) -> Nature:
        """Quick nature lookup.

        See https://pokeapi.co/docsv2/#natures for attributes and more detailed
        information.
        """
        return await self.get_resource('nature', resource)

    async def pokeathlon_stat(self, resource: Resource) -> PokeathlonStat:
        """Quick pokeathlon-stat lookup.

        See https://pokeapi.co/docsv2/#pokeathlon-stats for attributes and more
        detailed information.
        """
        return await self.get_resource('pokeathlon-stat', resource)

    async def pokemon(self, resource: Resource) -> Pokemon:
        """Quick pokemon lookup.

        See https://pokeapi.co/docsv2/#pokemon for attributes and more detailed
        information.
        """
        pkmn = await self.get_resource('pokemon', resource)
        pokeapi_data = await self.get_json(pkmn.location_area_encounters)
        pkmn.location_area_encounters = new_pokeapimetadata(
            'location_area_encounters', pokeapi_data
        )
        return pkmn

    async def pokemon_color(self, resource: Resource) -> PokemonColor:
        """Quick pokemon-color lookup.

        See https://pokeapi.co/docsv2/#pokemon-colors for attributes and more
        detailed information.
        """
        return await self.get_resource('pokemon-color', resource)

    async def pokemon_form(self, resource: Resource) -> PokemonForm:
        """Quick pokemon-form lookup.

        See https://pokeapi.co/docsv2/#pokemon-forms for attributes and more
        detailed information.
        """
        return await self.get_resource('pokemon-form', resource)

    async def pokemon_habitat(self, resource: Resource) -> PokemonHabitat:
        """Quick pokemon-habitat lookup.

        See https://pokeapi.co/docsv2/#pokemon-habitats for attributes and more
        detailed information.
        """
        return await self.get_resource('pokemon-habitat', resource)

    async def pokemon_shape(self, resource: Resource) -> PokemonShape:
        """Quick pokemon-shape lookup.

        See https://pokeapi.co/docsv2/#pokemon-shapes for attributes and more
        detailed information.
        """
        return await self.get_resource('pokemon-shape', resource)

    async def pokemon_species(self, resource: Resource) -> PokemonSpecies:
        """Quick pokemon-species lookup.

        See https://pokeapi.co/docsv2/#pokemon-species for attributes and more
        detailed information.
        """
        pkmn = await self.get_resource('pokemon-species', resource)
        pokeapi_data = await self.get_json(pkmn.evolution_chain)
        pkmn.evolution_chain = new_pokeapimetadata('evolution_chain', pokeapi_data)
        return pkmn

    async def stat(self, resource: Resource) -> Stat:
        """Quick stat lookup.

        See https://pokeapi.co/docsv2/#stats for attributes and more detailed
        information.
        """
        return await self.get_resource('stat', resource)

    async def type_(self, resource: Resource) -> Type:
        """Quick type lookup.

        See https://pokeapi.co/docsv2/#types for attributes and more detailed
        information.
        """
        return await self.get_resource('type', resource)

    async def language(self, resource: Resource) -> Language:
        """Quick language lookup.

        See https://pokeapi.co/docsv2/#languages for attributes and more detailed
        information.
        """
        return await self.get_resource('language', resource)
    
    async def __aenter__(self) -> 'PokeAPISession':
        """Just exists for type hinting."""
        return await super().__aenter__()


async def test():
    import asyncio
    async with PokeAPISession() as session:
        mons = await session.get_all_resources('pokemon')
        breloom = await session.pokemon('breloom')
        mega_punch = await session.move('mega-punch')
        mon_coros = tuple(session.pokemon(res['name'])
                          for res in mons['results']
                          if res['name'].startswith('a'))
        all_res = await asyncio.gather(*mon_coros)
        b = 0


if __name__ == '__main__':
    import asyncio
    asyncio.run(test())

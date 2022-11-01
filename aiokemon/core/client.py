import json
from typing import Optional, Union

from aiokemon.core.api import PokeAPIResource, new_pokeapimetadata
from aiokemon.core.common import Resource
from aiokemon.endpoints import *

from aiokemon.core.base_client import PokeAPIClientBase, gather_with_progress

Resource = Union[str, int]


class PokeAPIClient(PokeAPIClientBase):
    """Main session manager for PokéAPI. Contains a variety of functions that
    return type-hinted endpoint classes.
    """

    async def get_resource(self, endpoint: str,
                           resource: Optional[Resource] = None,
                           querystring: Optional[str] = None
                           ) -> PokeAPIResource:
        """Gets JSON data from the PokeAPI server and loads it into a
        PokeAPIResource object.
        """
        pokeapi_data = await self._get_json(endpoint, resource, querystring)
        return PokeAPIResource(endpoint, pokeapi_data)

    async def berry(self, resource: Resource) -> Berry:
        """Returns a berry resource.

        See https://pokeapi.co/docsv2/#berries for attributes and more detailed
        information.
        """
        return await self.get_resource('berry', resource)

    async def berry_firmness(self, resource: Resource) -> BerryFirmness:
        """Returns a berry-firmness resource.

        See https://pokeapi.co/docsv2/#berry-firmnesses for attributes and more
        detailed information.
        """
        return await self.get_resource('berry-firmness', resource)

    async def berry_flavor(self, resource: Resource) -> BerryFlavor:
        """Returns a berry-flavor resource.

        See https://pokeapi.co/docsv2/#berry-flavors for attributes and more
        detailed information.
        """
        return await self.get_resource('berry-flavor', resource)

    async def contest_type(self, resource: Resource) -> ContestType:
        """Returns a contest-type resource.

        See https://pokeapi.co/docsv2/#contest-types for attributes and more
        detailed information.
        """
        return await self.get_resource('contest-type', resource)

    async def contest_effect(self, id_: int) -> ContestEffect:
        """Returns a contest-effect resource.

        See https://pokeapi.co/docsv2/#contest-effects for attributes and more
        detailed information.
        """
        return await self.get_resource('contest-effect', id_)

    async def super_contest_effect(self, id_: int) -> SuperContestEffect:
        """Returns a super-contest-effect resource.

        See https://pokeapi.co/docsv2/#super-contest-effects for attributes and
        more detailed information.
        """
        return await self.get_resource('super-contest-effect', id_)

    async def encounter_method(self, resource: Resource) -> EncounterMethod:
        """Returns a encounter-method resource.

        See https://pokeapi.co/docsv2/#encounter-methods for attributes and
        more detailed information.
        """
        return await self.get_resource('encounter-method', resource)

    async def encounter_condition(self, resource: Resource,
                                  ) -> EncounterCondition:
        """Returns a encounter-condition resource.

        See https://pokeapi.co/docsv2/#encounter-conditions for attributes and
        more detailed information.
        """
        return await self.get_resource('encounter-condition', resource)

    async def encounter_condition_value(self, resource: Resource,
                                        ) -> EncounterConditionValue:
        """Returns a encounter-condition-value resource.

        See https://pokeapi.co/docsv2/#encounter-condition-values for
        attributes and more detailed information.
        """
        return await self.get_resource('encounter-condition-value', resource)

    async def evolution_chain(self, id_: int) -> EvolutionChain:
        """Returns a evolution-chain resource.

        See https://pokeapi.co/docsv2/#evolution-chains for attributes and more
        detailed information.
        """
        return await self.get_resource('evolution-chain', id_)

    async def evolution_trigger(self, resource: Resource) -> EvolutionTrigger:
        """Returns a evolution-trigger resource.

        See https://pokeapi.co/docsv2/#evolution-triggers for attributes and
        more detailed information.
        """
        return await self.get_resource('evolution-trigger', resource)

    async def generation(self, resource: Resource) -> Generation:
        """Returns a generation resource.

        See https://pokeapi.co/docsv2/#generations for attributes and more
        detailed information.
        """
        return await self.get_resource('generation', resource)

    async def pokedex(self, resource: Resource) -> Pokedex:
        """Returns a pokedex resource.

        See https://pokeapi.co/docsv2/#pokedexes for attributes and more
        detailed information.
        """
        return await self.get_resource('pokedex', resource)

    async def version(self, resource: Resource) -> Version:
        """Returns a version resource.

        See https://pokeapi.co/docsv2/#versions for attributes and more
        detailed information.
        """
        return await self.get_resource('version', resource)

    async def version_group(self, resource: Resource) -> VersionGroup:
        """Returns a version-group resource.

        See https://pokeapi.co/docsv2/#version-groups for attributes and more
        detailed information.
        """
        return await self.get_resource('version-group', resource)

    async def item(self, resource: Resource) -> Item:
        """Returns a item resource.

        See https://pokeapi.co/docsv2/#items for attributes and more detailed
        information.
        """
        return await self.get_resource('item', resource)

    async def item_attribute(self, resource: Resource) -> ItemAttribute:
        """Returns a item-attribute resource.

        See https://pokeapi.co/docsv2/#item-attributes for attributes and more
        detailed information.
        """
        return await self.get_resource('item-attribute', resource)

    async def item_category(self, resource: Resource) -> ItemCategory:
        """Returns a item-category resource.

        See https://pokeapi.co/docsv2/#item-categories for attributes and more
        detailed information.
        """
        return await self.get_resource('item-category', resource)

    async def item_fling_effect(self, resource: Resource) -> ItemFlingEffect:
        """Returns a item-fling-effect resource.

        See https://pokeapi.co/docsv2/#item-fling-effects for attributes and
        more detailed information.
        """
        return await self.get_resource('item-fling-effect', resource)

    async def item_pocket(self, resource: Resource) -> ItemPocket:
        """Returns a item-pocket resource.

        See https://pokeapi.co/docsv2/#item-pockets for attributes and more
        detailed information.
        """
        return await self.get_resource('item-pocket', resource)

    async def machine(self, id_: int) -> Machine:
        """Returns a machine resource.

        See https://pokeapi.co/docsv2/#machines for attributes and more
        detailed information.
        """
        return await self.get_resource('machine', id_)

    async def move(self, resource: Resource) -> Move:
        """Returns a move resource.

        See https://pokeapi.co/docsv2/#moves for attributes and more detailed
        information.
        """
        return await self.get_resource('move', resource)

    async def move_ailment(self, resource: Resource) -> MoveAilment:
        """Returns a move-ailment resource.

        See https://pokeapi.co/docsv2/#move-ailments for attributes and more
        detailed information.
        """
        return await self.get_resource('move-ailment', resource)

    async def move_battle_style(self, resource: Resource) -> MoveBattleStyle:
        """Returns a move-battle-style resource.

        See https://pokeapi.co/docsv2/#move-battle-styles for attributes and
        more detailed information.
        """
        return await self.get_resource('move-battle-style', resource)

    async def move_category(self, resource: Resource) -> MoveCategory:
        """Returns a move-category resource.

        See https://pokeapi.co/docsv2/#move-categories for attributes and more
        detailed information.
        """
        return await self.get_resource('move-category', resource)

    async def move_damage_class(self, resource: Resource) -> MoveDamageClass:
        """Returns a move-damage-class resource.

        See https://pokeapi.co/docsv2/#move-damage-classes for attributes and
        more detailed information.
        """
        return await self.get_resource('move-damage-class', resource)

    async def move_learn_method(self, resource: Resource) -> MoveLearnMethod:
        """Returns a move-learn-method resource.

        See https://pokeapi.co/docsv2/#move-learn-methods for attributes and
        more detailed information.
        """
        return await self.get_resource('move-learn-method', resource)

    async def move_target(self, resource: Resource) -> MoveTarget:
        """Returns a move-target resource.

        See https://pokeapi.co/docsv2/#move-targets for attributes and more
        detailed information.
        """
        return await self.get_resource('move-target', resource)

    async def location(self, id_: int) -> Location:
        """Returns a location resource.

        See https://pokeapi.co/docsv2/#locations for attributes and more
        detailed information.
        """
        return await self.get_resource('location', id_)

    async def location_area(self, id_: int) -> LocationArea:
        """Returns a location-area resource.

        See https://pokeapi.co/docsv2/#location-areas for attributes and more
        detailed information.
        """
        return await self.get_resource('location-area', id_)

    async def pal_park_area(self, resource: Resource) -> PalParkArea:
        """Returns a pal-park-area resource.

        See https://pokeapi.co/docsv2/#pal-park-areas for attributes and more
        detailed information.
        """
        return await self.get_resource('pal-park-area', resource)

    async def region(self, resource: Resource) -> Region:
        """Returns a region resource.

        See https://pokeapi.co/docsv2/#regions for attributes and more detailed
        information.
        """
        return await self.get_resource('region', resource)

    async def ability(self, resource: Resource) -> Ability:
        """Returns a ability resource.

        See https://pokeapi.co/docsv2/#abilities for attributes and more
        detailed information.
        """
        return await self.get_resource('ability', resource)

    async def characteristic(self, id_: int) -> Characteristic:
        """Returns a characteristic resource.

        See https://pokeapi.co/docsv2/#characteristics for attributes and more
        detailed information.
        """
        return await self.get_resource('characteristic', id_)

    async def egg_group(self, resource: Resource) -> EggGroup:
        """Returns a egg-group resource.

        See https://pokeapi.co/docsv2/#egg-groups for attributes and more
        detailed information.
        """
        return await self.get_resource('egg-group', resource)

    async def gender(self, resource: Resource) -> Gender:
        """Returns a gender resource.

        See https://pokeapi.co/docsv2/#genders for attributes and more detailed
        information.
        """
        return await self.get_resource('gender', resource)

    async def growth_rate(self, resource: Resource) -> GrowthRate:
        """Returns a growth-rate resource.

        See https://pokeapi.co/docsv2/#growth-rates for attributes and more
        detailed information.
        """
        return await self.get_resource('growth-rate', resource)

    async def nature(self, resource: Resource) -> Nature:
        """Returns a nature resource.

        See https://pokeapi.co/docsv2/#natures for attributes and more detailed
        information.
        """
        return await self.get_resource('nature', resource)

    async def pokeathlon_stat(self, resource: Resource) -> PokeathlonStat:
        """Returns a pokeathlon-stat resource.

        See https://pokeapi.co/docsv2/#pokeathlon-stats for attributes and more
        detailed information.
        """
        return await self.get_resource('pokeathlon-stat', resource)

    async def pokemon(self, resource: Resource) -> Pokemon:
        """Returns a pokemon resource.

        See https://pokeapi.co/docsv2/#pokemon for attributes and more detailed
        information.
        """
        pkmn = await self.get_resource('pokemon', resource)
        pokeapi_data = await self._get_response_text(
            'pokemon', url=pkmn.location_area_encounters
        )
        pkmn.location_area_encounters = new_pokeapimetadata(
            'location_area_encounters', json.loads(pokeapi_data)
        )
        return pkmn

    async def pokemon_color(self, resource: Resource) -> PokemonColor:
        """Returns a pokemon-color resource.

        See https://pokeapi.co/docsv2/#pokemon-colors for attributes and more
        detailed information.
        """
        return await self.get_resource('pokemon-color', resource)

    async def pokemon_form(self, resource: Resource) -> PokemonForm:
        """Returns a pokemon-form resource.

        See https://pokeapi.co/docsv2/#pokemon-forms for attributes and more
        detailed information.
        """
        return await self.get_resource('pokemon-form', resource)

    async def pokemon_habitat(self, resource: Resource) -> PokemonHabitat:
        """Returns a pokemon-habitat resource.

        See https://pokeapi.co/docsv2/#pokemon-habitats for attributes and more
        detailed information.
        """
        return await self.get_resource('pokemon-habitat', resource)

    async def pokemon_shape(self, resource: Resource) -> PokemonShape:
        """Returns a pokemon-shape resource.

        See https://pokeapi.co/docsv2/#pokemon-shapes for attributes and more
        detailed information.
        """
        return await self.get_resource('pokemon-shape', resource)

    async def pokemon_species(self, resource: Resource) -> PokemonSpecies:
        """Returns a pokemon-species resource.

        See https://pokeapi.co/docsv2/#pokemon-species for attributes and more
        detailed information.
        """
        pkmn = await self.get_resource('pokemon-species', resource)
        pokeapi_data = await self._get_response_text(
            'evolution-chain', url=pkmn.evolution_chain.url
        )
        pkmn.evolution_chain = new_pokeapimetadata(
            'evolution_chain', json.loads(pokeapi_data)
        )
        return pkmn

    async def stat(self, resource: Resource) -> Stat:
        """Returns a stat resource.

        See https://pokeapi.co/docsv2/#stats for attributes and more detailed
        information.
        """
        return await self.get_resource('stat', resource)

    async def type_(self, resource: Resource) -> Type:
        """Returns a type resource.

        See https://pokeapi.co/docsv2/#types for attributes and more detailed
        information.
        """
        return await self.get_resource('type', resource)

    async def language(self, resource: Resource) -> Language:
        """Returns a language resource.

        See https://pokeapi.co/docsv2/#languages for attributes and more
        detailed information.
        """
        return await self.get_resource('language', resource)

    async def __aenter__(self) -> 'PokeAPIClient':
        """Just exists for type hinting."""
        return await super().__aenter__()


if __name__ == '__main__':
    import asyncio

    async def test_session():
        async with PokeAPIClient() as session:
            mons = await session.get_available_resources('pokemon')
            mon_coros = tuple(session.pokemon(res['name'])
                              for res in mons['results'])
            all_mons = await gather_with_progress(mon_coros)

            moves = await session.get_available_resources('move')
            move_coros = tuple(session.move(res['name'])
                               for res in moves['results'])
            all_moves = await gather_with_progress(move_coros)

            a = 0

    async def test_matcher():
        async with PokeAPIClient() as session:
            await session.pokemon('brelom')
            await session.pokemon('drilfoon')
            await session.pokemon('vileplume')
            await session.pokemon('bouldore')
            await session.pokemon('garchom')
            b = 0

    asyncio.run(test_session())

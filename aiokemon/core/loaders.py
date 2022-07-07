"""
This file is an async-ified version of the code found in Pokebase.
The commit from which I copied the code can be found here:
https://github.com/PokeAPI/pokebase/blob/dbd3b6b66b919740d1f710e729eb98f3930fa522/pokebase/loaders.py

Note that some of the type hinting of this file is a bit misleading. For
example, the pokemon() function doesn't actually return an instance of
class Pokemon, it returns an APIResource. However, once that APIResource is
loaded, all of the attributes hinted in the Pokemon class should be populated.

TODO: Add custom loading for:
item.baby_trigger_for
move.contest_effect
move.super_contest_effect
pokemon.location_area_encounters
pokemon_species.evolution_chain
stat.characteristics
"""

from aiokemon.core.api import get_resource, get_subresource
from aiokemon.core.common import Resource
from aiokemon.endpoints import *


async def berry(resource: Resource, **kwargs) -> Berry:
    """Quick berry lookup.

    See https://pokeapi.co/docsv2/#berries for attributes and more detailed
    information.
    """
    return await get_resource("berry", resource, **kwargs)


async def berry_firmness(resource: Resource, **kwargs) -> BerryFirmness:
    """Quick berry-firmness lookup.

    See https://pokeapi.co/docsv2/#berry-firmnesses for attributes and more
    detailed information.
    """
    return await get_resource("berry-firmness", resource, **kwargs)


async def berry_flavor(resource: Resource, **kwargs) -> BerryFlavor:
    """Quick berry-flavor lookup.

    See https://pokeapi.co/docsv2/#berry-flavors for attributes and more
    detailed information.
    """
    return await get_resource("berry-flavor", resource, **kwargs)


async def contest_type(resource: Resource, **kwargs) -> ContestType:
    """Quick contest-type lookup.

    See https://pokeapi.co/docsv2/#contest-types for attributes and more
    detailed information.
    """
    return await get_resource("contest-type", resource, **kwargs)


async def contest_effect(id_: int, **kwargs) -> ContestEffect:
    """Quick contest-effect lookup.

    See https://pokeapi.co/docsv2/#contest-effects for attributes and more
    detailed information.
    """
    return await get_resource("contest-effect", id_, **kwargs)


async def super_contest_effect(id_: int, **kwargs) -> SuperContestEffect:
    """Quick super-contest-effect lookup.

    See https://pokeapi.co/docsv2/#super-contest-effects for attributes and
    more detailed information.
    """
    return await get_resource("super-contest-effect", id_, **kwargs)


async def encounter_method(resource: Resource, **kwargs) -> EncounterMethod:
    """Quick encounter-method lookup.

    See https://pokeapi.co/docsv2/#encounter-methods for attributes and more
    detailed information.
    """
    return await get_resource("encounter-method", resource, **kwargs)


async def encounter_condition(resource: Resource, **kwargs
                              ) -> EncounterCondition:
    """Quick encounter-condition lookup.

    See https://pokeapi.co/docsv2/#encounter-conditions for attributes and more
    detailed information.
    """
    return await get_resource("encounter-condition", resource, **kwargs)


async def encounter_condition_value(resource: Resource, **kwargs
                                    ) -> EncounterConditionValue:
    """Quick encounter-condition-value lookup.

    See https://pokeapi.co/docsv2/#encounter-condition-values for attributes
    and more detailed information.
    """
    return await get_resource("encounter-condition-value", resource, **kwargs)


async def evolution_chain(id_: int, **kwargs) -> EvolutionChain:
    """Quick evolution-chain lookup.

    See https://pokeapi.co/docsv2/#evolution-chains for attributes and more
    detailed information.
    """
    return await get_resource("evolution-chain", id_, **kwargs)


async def evolution_trigger(resource: Resource, **kwargs) -> EvolutionTrigger:
    """Quick evolution-trigger lookup.

    See https://pokeapi.co/docsv2/#evolution-triggers for attributes and more
    detailed information.
    """
    return await get_resource("evolution-trigger", resource, **kwargs)


async def generation(resource: Resource, **kwargs) -> Generation:
    """Quick generation lookup.

    See https://pokeapi.co/docsv2/#generations for attributes and more detailed
    information.
    """
    return await get_resource("generation", resource, **kwargs)


async def pokedex(resource: Resource, **kwargs) -> Pokedex:
    """Quick pokedex lookup.

    See https://pokeapi.co/docsv2/#pokedexes for attributes and more detailed
    information.
    """
    return await get_resource("pokedex", resource, **kwargs)


async def version(resource: Resource, **kwargs) -> Version:
    """Quick version lookup.

    See https://pokeapi.co/docsv2/#versions for attributes and more detailed
    information.
    """
    return await get_resource("version", resource, **kwargs)


async def version_group(resource: Resource, **kwargs) -> VersionGroup:
    """Quick version-group lookup.

    See https://pokeapi.co/docsv2/#version-groups for attributes and more
    detailed information.
    """
    return await get_resource("version-group", resource, **kwargs)


async def item(resource: Resource, **kwargs) -> Item:
    """Quick item lookup.

    See https://pokeapi.co/docsv2/#items for attributes and more detailed
    information.
    """
    return await get_resource("item", resource, **kwargs)


async def item_attribute(resource: Resource, **kwargs) -> ItemAttribute:
    """Quick item-attribute lookup.

    See https://pokeapi.co/docsv2/#item-attributes for attributes and more
    detailed information.
    """
    return await get_resource("item-attribute", resource, **kwargs)


async def item_category(resource: Resource, **kwargs) -> ItemCategory:
    """Quick item-category lookup.

    See https://pokeapi.co/docsv2/#item-categories for attributes and more
    detailed information.
    """
    return await get_resource("item-category", resource, **kwargs)


async def item_fling_effect(resource: Resource, **kwargs) -> ItemFlingEffect:
    """Quick item-fling-effect lookup.

    See https://pokeapi.co/docsv2/#item-fling-effects for attributes and more
    detailed information.
    """
    return await get_resource("item-fling-effect", resource, **kwargs)


async def item_pocket(resource: Resource, **kwargs) -> ItemPocket:
    """Quick item-pocket lookup.

    See https://pokeapi.co/docsv2/#item-pockets for attributes and more
    detailed information.
    """
    return await get_resource("item-pocket", resource, **kwargs)


async def machine(id_: int, **kwargs) -> Machine:
    """Quick machine lookup.

    See https://pokeapi.co/docsv2/#machines for attributes and more detailed
    information.
    """
    return await get_resource("machine", id_, **kwargs)


async def move(resource: Resource, **kwargs) -> Move:
    """Quick move lookup.

    See https://pokeapi.co/docsv2/#moves for attributes and more detailed
    information.
    """
    return await get_resource("move", resource, **kwargs)


async def move_ailment(resource: Resource, **kwargs) -> MoveAilment:
    """Quick move-ailment lookup.

    See https://pokeapi.co/docsv2/#move-ailments for attributes and more
    detailed information.
    """
    return await get_resource("move-ailment", resource, **kwargs)


async def move_battle_style(resource: Resource, **kwargs) -> MoveBattleStyle:
    """Quick move-battle-style lookup.

    See https://pokeapi.co/docsv2/#move-battle-styles for attributes and more
    detailed information.
    """
    return await get_resource("move-battle-style", resource, **kwargs)


async def move_category(resource: Resource, **kwargs) -> MoveCategory:
    """Quick move-category lookup.

    See https://pokeapi.co/docsv2/#move-categories for attributes and more
    detailed information.
    """
    return await get_resource("move-category", resource, **kwargs)


async def move_damage_class(resource: Resource, **kwargs) -> MoveDamageClass:
    """Quick move-damage-class lookup.

    See https://pokeapi.co/docsv2/#move-damage-classes for attributes and more
    detailed information.
    """
    return await get_resource("move-damage-class", resource, **kwargs)


async def move_learn_method(resource: Resource, **kwargs) -> MoveLearnMethod:
    """Quick move-learn-method lookup.

    See https://pokeapi.co/docsv2/#move-learn-methods for attributes and more
    detailed information.
    """
    return await get_resource("move-learn-method", resource, **kwargs)


async def move_target(resource: Resource, **kwargs) -> MoveTarget:
    """Quick move-target lookup.

    See https://pokeapi.co/docsv2/#move-targets for attributes and more
    detailed information.
    """
    return await get_resource("move-target", resource, **kwargs)


async def location(id_: int, **kwargs) -> Location:
    """Quick location lookup.

    See https://pokeapi.co/docsv2/#locations for attributes and more detailed
    information.
    """
    return await get_resource("location", id_, **kwargs)


async def location_area(id_: int, **kwargs) -> LocationArea:
    """Quick location-area lookup.

    See https://pokeapi.co/docsv2/#location-areas for attributes and more
    detailed information.
    """
    return await get_resource("location-area", id_, **kwargs)


async def pal_park_area(resource: Resource, **kwargs) -> PalParkArea:
    """Quick pal-park-area lookup.

    See https://pokeapi.co/docsv2/#pal-park-areas for attributes and more
    detailed information.
    """
    return await get_resource("pal-park-area", resource, **kwargs)


async def region(resource: Resource, **kwargs) -> Region:
    """Quick region lookup.

    See https://pokeapi.co/docsv2/#regions for attributes and more detailed
    information.
    """
    return await get_resource("region", resource, **kwargs)


async def ability(resource: Resource, **kwargs) -> Ability:
    """Quick ability lookup.

    See https://pokeapi.co/docsv2/#abilities for attributes and more detailed
    information.
    """
    return await get_resource("ability", resource, **kwargs)


async def characteristic(id_: int, **kwargs) -> Characteristic:
    """Quick characteristic lookup.

    See https://pokeapi.co/docsv2/#characteristics for attributes and more
    detailed information.
    """
    return await get_resource("characteristic", id_, **kwargs)


async def egg_group(resource: Resource, **kwargs) -> EggGroup:
    """Quick egg-group lookup.

    See https://pokeapi.co/docsv2/#egg-groups for attributes and more detailed
    information.
    """
    return await get_resource("egg-group", resource, **kwargs)


async def gender(resource: Resource, **kwargs) -> Gender:
    """Quick gender lookup.

    See https://pokeapi.co/docsv2/#genders for attributes and more detailed
    information.
    """
    return await get_resource("gender", resource, **kwargs)


async def growth_rate(resource: Resource, **kwargs) -> GrowthRate:
    """Quick growth-rate lookup.

    See https://pokeapi.co/docsv2/#growth-rates for attributes and more
    detailed information.
    """
    return await get_resource("growth-rate", resource, **kwargs)


async def nature(resource: Resource, **kwargs) -> Nature:
    """Quick nature lookup.

    See https://pokeapi.co/docsv2/#natures for attributes and more detailed
    information.
    """
    return await get_resource("nature", resource, **kwargs)


async def pokeathlon_stat(resource: Resource, **kwargs) -> PokeathlonStat:
    """Quick pokeathlon-stat lookup.

    See https://pokeapi.co/docsv2/#pokeathlon-stats for attributes and more
    detailed information.
    """
    return await get_resource("pokeathlon-stat", resource, **kwargs)


async def pokemon(resource: Resource, **kwargs) -> Pokemon:
    """Quick pokemon lookup.

    See https://pokeapi.co/docsv2/#pokemon for attributes and more detailed
    information.
    """
    pkmn = await get_resource("pokemon", resource, **kwargs)
    pkmn.location_area_encounters = await get_subresource(
        'location_area_encounters', pkmn.location_area_encounters
    )
    return pkmn


async def pokemon_color(resource: Resource, **kwargs) -> PokemonColor:
    """Quick pokemon-color lookup.

    See https://pokeapi.co/docsv2/#pokemon-colors for attributes and more
    detailed information.
    """
    return await get_resource("pokemon-color", resource, **kwargs)


async def pokemon_form(resource: Resource, **kwargs) -> PokemonForm:
    """Quick pokemon-form lookup.

    See https://pokeapi.co/docsv2/#pokemon-forms for attributes and more
    detailed information.
    """
    return await get_resource("pokemon-form", resource, **kwargs)


async def pokemon_habitat(resource: Resource, **kwargs) -> PokemonHabitat:
    """Quick pokemon-habitat lookup.

    See https://pokeapi.co/docsv2/#pokemon-habitats for attributes and more
    detailed information.
    """
    return await get_resource("pokemon-habitat", resource, **kwargs)


async def pokemon_shape(resource: Resource, **kwargs) -> PokemonShape:
    """Quick pokemon-shape lookup.

    See https://pokeapi.co/docsv2/#pokemon-shapes for attributes and more
    detailed information.
    """
    return await get_resource("pokemon-shape", resource, **kwargs)


async def pokemon_species(resource: Resource, **kwargs) -> PokemonSpecies:
    """Quick pokemon-species lookup.

    See https://pokeapi.co/docsv2/#pokemon-species for attributes and more
    detailed information.
    """
    pkmn = await get_resource("pokemon-species", resource, **kwargs)
    pkmn.evolution_chain = await get_subresource(
        'evolution_chain', pkmn.evolution_chain.url
    )
    return pkmn


async def stat(resource: Resource, **kwargs) -> Stat:
    """Quick stat lookup.

    See https://pokeapi.co/docsv2/#stats for attributes and more detailed
    information.
    """
    return await get_resource("stat", resource, **kwargs)


async def type_(resource: Resource, **kwargs) -> Type:
    """Quick type lookup.

    See https://pokeapi.co/docsv2/#types for attributes and more detailed
    information.
    """
    return await get_resource("type", resource, **kwargs)


async def language(resource: Resource, **kwargs) -> Language:
    """Quick language lookup.

    See https://pokeapi.co/docsv2/#languages for attributes and more detailed
    information.
    """
    return await get_resource("language", resource, **kwargs)

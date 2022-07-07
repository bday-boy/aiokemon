# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class PokemonSpeciesVariety:
    is_default: bool
    pokemon: NamedAPIResource


class PalParkEncounterArea:
    base_score: int
    rate: int
    area: NamedAPIResource


class PokemonSpeciesDexEntry:
    entry_number: int
    pokedex: NamedAPIResource


class Genus:
    genus: str
    language: NamedAPIResource


class PokemonSpecies(PokeAPIResource):
    id: int
    name: str
    order: int
    gender_rate: int
    capture_rate: int
    base_happiness: int
    is_baby: bool
    is_legendary: bool
    is_mythical: bool
    hatch_counter: int
    has_gender_differences: bool
    forms_switchable: bool
    growth_rate: NamedAPIResource
    pokedex_numbers: List[PokemonSpeciesDexEntry]
    egg_groups: List[NamedAPIResource]
    color: NamedAPIResource
    shape: NamedAPIResource
    evolves_from_species: NamedAPIResource
    evolution_chain: APIResource
    habitat: NamedAPIResource
    generation: NamedAPIResource
    names: List[Name]
    pal_park_encounters: List[PalParkEncounterArea]
    flavor_text_entries: List[FlavorText]
    form_descriptions: List[Description]
    genera: List[Genus]
    varieties: List[PokemonSpeciesVariety]

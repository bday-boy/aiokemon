# This file was generated automatically.
from typing import List

from aiokemon.core.api import PokeAPIResource
from aiokemon.endpoints.utility.common_models import *


class NaturePokeathlonStatAffect:
    max_change: int
    nature: NamedAPIResource


class NaturePokeathlonStatAffectSets:
    increase: List[NaturePokeathlonStatAffect]
    decrease: List[NaturePokeathlonStatAffect]


class PokeathlonStat(PokeAPIResource):
    id: int
    name: str
    names: List[Name]
    affecting_natures: NaturePokeathlonStatAffectSets

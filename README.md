# aiokemon

__aiokemon__ is an asynchronous Python wrapper for making PokéAPI requests.

It took a lot of inspiration from
[Pokebase](https://github.com/PokeAPI/pokebase), so huge thanks to everyone
who contributed to that project. I only didn't make a fork because enough of
the code base is different that refactoring it would've been more effort than
just working from scratch. I might make a fork in the future just cuz I feel
like a jerk for stealing so many of their ideas/syntax and not forking the
original repo cuz I'm lazy.

## Features

- Ability to interface with other asynchronous frameworks, such as Discord.py
  (which is why I made this library in the first place)
- Easy lookup of resource attributes via the `.` operator
- Can use basic fuzzy string matching to correct small typos and fit
  nonexistent resource names to correct ones, i.e. `gardevor` →
  `gardevoir` or even `Shield Aegislash` → `aegislash-shield`

## Key Differences From Pokebase

### aiokemon isn't lazy

Pokebase offers a clever method of lazily loading certain resource attributes
as they are requested by the user. For example:

```python
>>> import pokebase as pb
>>> breloom = pb.pokemon('breloom')
>>> breloom.abilities[0].ability.name
'effect-spore'
>>> # this ability is also a resource in itself, so even though its attributes
>>> # aside from "name" and "url" aren't immediately available from the scope
>>> # of the pokemon endpoint, we can still do this:
>>> breloom.abilities[0].ability.pokemon[0].pokemon.name
'vileplume'
>>> # Pokebase loaded the effect-spore resource behind the scenes so now we
>>> # can treat that entry as its own entire resource
```

However, due to the nature of async and also my tiny brain, Python's magic
methods can't easily (or often at all) be overloaded with async versions.
Implementing lazy attribute loading like this behind the scenes just isn't
possible as far as I can tell (again, tiny brain). So the aiokemon version
of the above code is more like this (assume awaits are happening in an event
loop or something idk):

```python
>>> import aiokemon as ak
>>> breloom = await ak.pokemon('breloom')
>>> breloom.abilities[0].ability.name
'effect-spore'
>>> # now we try to get an attribute that isn't there yet, just like before
>>> breloom.abilities[0].ability.pokemon[0].pokemon.name
AttributeError: 'APIMetaData' object has no attribute 'pokemon'
>>> # uh oh, no lazy loading. But instead, we can do this
>>> ability = await breloom.abilities[0].ability.as_resource()
>>> ability.pokemon[0].pokemon.name
'vileplume'
```

So this version requires more explicit code on the user's part, but still
functions very similarly to Pokebase.

### Fuzzy String Matching

As mentioned in __Features__, aiokemon can fix small errors in resource names.
This functionality can be toggled by changing the `FIND_MATCH` variable.
Resources that are an exact match will be returned immediately, so
matching doesn't cause much overhead when resource requests are exact
matches for ones.

Once again, this functionality was meant to improve the ability of this
library to interface with Discord.py. With fuzzy string matching, PokeAPI can
be used to search for Pokemon information even with small errors (for example,
a person searching for move information through a Discord bot).

## Development Status

WIP :)

## Installation

None yet.

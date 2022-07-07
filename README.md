# aiokemon

[![License](https://img.shields.io/github/license/bday-boy/aiokemon?style=for-the-badge)](./LICENSE)

__aiokemon__ is an asynchronous Python wrapper for making PokéAPI requests.

It took a lot of inspiration from
[Pokebase](https://github.com/PokeAPI/pokebase), so huge thanks to everyone
who contributed to that project. I only didn't make a fork because enough of
the code base is different that refactoring it would've been more effort than
just working from scratch.

## Features

- Ability to interface with other asynchronous frameworks, such as Discord.py
  (which is why I made this library in the first place)
- Easy lookup of resource attributes via the `.` operator
- Can use basic fuzzy string matching to correct small typos and fit
  nonexistent resource names to correct ones, i.e. `gardevor` →
  `gardevoir` or even `Shield Aegislash` → `aegislash-shield`
- Full type hinting of resources and their attributes

## Usage

aiokemon is so similar to Pokebase that it can essentially be used as a
drop-in. So, as one might imagine, its syntax is very similar as well.

For example, if we want to get a Pokémon:

```python
>>> import aiokemon as ak
>>> breloom = await ak.pokemon('breloom')
>>> breloom
<pokemon-breloom>
>>> breloom.abilities[0].ability.name
'effect-spore'
>>> breloom.attrs # shows PokéAPI data attributes
['abilities', 'base_experience', 'forms', 'game_indices', 'height', 'held_items', 'id', 'is_default', 'location_area_encounters', 'moves', 'name', 'order', 'past_types', 'species', 'sprites', 'stats', 'types', 'url', 'weight']
```

Suppose we decide to get one of its moves as well:

```python
>>> mega_punch = await breloom.moves[0].move.as_resource()
>>> mega_punch.accuracy
85
>>> mega_punch.target.name
'selected-pokemon'
```

And it's as easy as that.

### Type Hinting

While still in development, aiokemon has support for fully type-hinted
resources. Here is an example in VSCode:

![Pokemon endpoint type hint example](./images/type%20hinting%20example.png)

However, there are some important things to note about the type hinting:

- Only each endpoint's specific wrapper function will return a class with the
  included attributes.
- The type hinting is achieved by creating empty classes with typed instance
  variables. In other words, the classes returned from the wrapper functions
  aren't actually 
- All type hinting classes are scraped from the PokéAPI docs page. However,
  the docs page actually has some errors. For example, in the
  [pokemon sprites](https://pokeapi.co/docs/v2#pokemonsprites) resource
  (this link has an element ID in it but doesn't actually scroll, so on
  the page sidebar just click Pokemon -> Pokemon and scroll a bit to
  PokemonSprites), it says all fields can be strings. However, Pokemon with
  only one gender or no gender will have `None` for all the *_female entries,
  so expecting an empty string and calling `str`-specific functions on it will
  raise an `AttributeError`.

That being said, in the original usage example, if you want to get type hinting
for Mega Punch, then you should do `ak.move(breloom.moves[0].move.name)`
instead.

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
>>> # Pokebase loaded the effect-spore ability resource behind the scenes so
>>> # now we can treat that attribute as its own entire resource
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
This functionality cannot be toggled for now, but resources are returned
immediately when an exact match exists. This way, overhead only occurs with
inexact searches.

Once again, this functionality was meant to improve the ability of this
library to interface with Discord.py. With fuzzy string matching, PokeAPI can
be used to search for Pokemon information even with small errors (for example,
a person searching for move information through a Discord bot).

## Development Status

Version 1.0.0 "works." I haven't figured out Python unit tests yet, so it
could be buggy garbage for all I know.

## Installation

__aiokemon__ isn't hosted on PyPi yet, but installation is fairly
straightforward:

```python
python ./setup.py install
```

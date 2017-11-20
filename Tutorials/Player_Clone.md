# Player Character Cloning Tutorial

This tutorial will show you how to duplicate an existing player character and make a whole new character.
The simplest character, Fred, will be used.

First, the tutorial will walk you through the bare minimum required to make a player character.
Then, player sprites and animations are explained.
Finally, advanced player behaviors are briefly introduced.

## The bare minimum

For the game to recognize a new player character, the `Characters` directory must contain a file for that player, and that file must cointain that player's class.
`Characters/fred.py` contains the `Fred` class.
An easy way to create a new character is to create a copy of Fred.

Make a copy of `fred.py` and call it something like `bob.py`.
Then open `bob.py` and find the line that declares the `Fred` class:

```python
class Fred(Player):
    """
    Most basic playable character, Fred.
```

and change it to declare the `Bob` class instead:

```python
class Bob(Player):
    """
    Bob is a clone of Fred.
```

That's it.
You now have a player character named Bob that is otherwise completely identical to Fred.
The text following the `"""` is a docstring.
Write your own description of Bob there for future reference.
The game will automagically find Bob in the `Characters` directory and add him into the game as a power-up (in case you're interested, the code that does this is in the `get_subclasses()` function in `projectile-game.py`).

You can also set Bob to be the main player character when you start the game from the command line:

```
$> ./projectile-game.py -p Bob
```

If you set Bob as the main player, Fred will appear in the game as a power-up.

Now that you have a working player character, use what you learned in the [Player Tweak](Player_Tweak.md) tutorial to make Bob move differently from Fred.

## About sprites and animation

So far, you have created a new player, Bob, who looks like Fred but behaves differently.
What if you want to change how Bob looks?

The `images` dictionary in `bob.py` contains all the images of a player that the game draws to the screen.
At the moment, Bob looks like Fred, because Bob uses the same images as Fred:

```python
        images = {'neutral': 'Fred_neutral.png',
                  'walk': {'right': {'straight': ['Fred_walk_00.png',
                                                  'Fred_walk_02.png'],
                                     'up': ['Fred_walk_up_00.png',
                                            'Fred_walk_up_02.png'],
                                     'down': ['Fred_walk_down_00.png',
                                              'Fred_walk_down_02.png']}},
                  'stand': {'right': {'straight': ['Fred_stand.png'],
                                      'up': ['Fred_stand_up.png'],
                                      'down': ['Fred_stand_down.png']}},
                  'fly': {'right': {'straight': ['Fred_fly.png'],
                                    'up': ['Fred_fly_up.png'],
                                    'down': ['Fred_fly_down.png']}},
                  'dead': ['Fred_dead_00.png', 'Fred_dead_01.png',
                           'Fred_dead_02.png', 'Fred_dead_03.png']}
```

When Bob is in a neutral pose, the game uses `Fred_neutral.png`.
When Bob is walking right, the game uses one of the `Fred_walk_*.png` images, depending on whether Bob is looking straight ahead, up, or down, and where in the animation cycle Bob is.
When Bob is in mid-air, the game uses one of the `Fred_fly*.png` images.
All of the image files are in the `Images` directory.
Notice that there are no images for moving left.
When a player moves left, then by default, the game just mirrors the appropriate right-facing image.

In fact, the only image a player really needs is `neutral`&mdash;the game will fall back to `neutral` if the required image doesn't exist.
So, for example, you could draw one image of Bob and fill in the rest later.

```python
        images = {'neutral': 'Bob_neutral.png'}
```

What about animations?
Fred has animated walk cycles and an animated explosion death cycle.
For example, when walking forward and looking up, the game switches between `Fred_walk_down_00.png` and `Fred_walk_down_02.png`.
These two images are listed in an array: `[Fred_walk_down_00.png, Fred_walk_down_02.png]`.
Fred does not, however, have standing or flying animations; the arrays for these actions have only one entry (e.g., `['Fred_fly_up.png']`).

There is no limit to how long an animation array can be (but ridiculously long animtations might affect performance).
You can provide one image, like Fred when flying and looking up; a series of four images, like Fred's death cycle; or any other number.

Finally, a note on image size.
There are currently no programmed constraints on image size.
However, you should make sure that all of your player's images are the same size.
Fred, for example, is 18x24 pixels.
Players that are much smaller than this might be difficult to see on screen.
Players much larger than this might have trouble fitting past obstacles in levels.

## What else?

So you've cloned Fred to create your own player character, given this player its own movement characteristics, and drawn some graphics for your player, and you're wondering what else there is to do.
More complicated players require you to write new Python code to make that behavior happen, and, unfortunately, writing code is beyond the scope of this tutorial.
However, to get an idea of what's possible, take a look at Ilmar (in `Characters/ilmar.py`).

`ilmar.py` defines three extra functions: `fire()`, `got_hit()`, and `reset()`.
For a character like Fred, these functions are defined in `Classes/player.py`.
Both Fred and Ilmar are of the `Player` class, so they automatically have access to these functions.
(The `class Fred(Player):` statement in `fred.py` is what tells Python that Fred is of the `Player` class.)

Ilmar needs its own versions of these functions, because he has some special abilities.
Ilmar is a tank and cannot fire downward, and Ilmar sometimes explodes when firing.
Ilmar's `fire()` function makes this happen.
You can compare the `fire()` function in `ilmar.py` and the one in `player.py` to see what's different.
As a tank, Ilmar is also invincible.
Normal player characters get hurt when they are hit by projectiles, and this is handled by the `got_hit()` function.
Ilmar doesn't get hurt, and his `got_hit()` function is empty.
Finally, normal players are invincible for a short time after being reset, as shown by a green circle around the player.
Players are reset when they reappear in the game after being replaced by a player from a power-up.
Since Ilmar is always invincible, his `reset()` function removes the green circle before the circle is displayed.


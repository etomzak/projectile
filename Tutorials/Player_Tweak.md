# Player Character Tweak Tutorial

This tutorial will show you how to tweak the behavior of an existing player character.
Player characters are ones that the player of the game controls, like Fred or Ilmar.
Player characters are located in the `Characters` directory within the main game directory.
Fred is the simplest player character, so this tutorial will use him.

First, the tutorial will explain how Fred is defined.
Then, it will show how Fred can be tweaked.

## Fred file overview

Fred is defined in the `fred.py` file in the `Characters` directory.
Open `fred.py` with your text editor of choice.
If you have worked with Python before, it's probably easiest to use whatever editor you used then.
Otherwise, Notepad on Windows, TextEdit on MacOS, or gEdit on Linux will work.

In Python, every line that starts with a `#` is a comment and can be ignored.

The `fred.py` file starts with:

```python
import sys, os

sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.player import Player
from Projectiles.bb import BB
```

Fred is a Player character that shoots BBs.
This code tells Python how to find out what `Player` and `BB` are.

Next:

```python
class Fred(Player):
```

This tells Python that Fred is a type of `Player`.
You can find the code for the player class in `Classes/player.py`, but that code is beyond the scope of this tutorial.

```python
    def __init__(self, kwargs):
```

The `__init__()` function is what is run to create a Fred character.

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

The `images` dictionary contains all the pictures of Fred that the game shows.
You can find all of the `.png` files in the `Images` directory.

```python
        kwargs["images"]                = images
        kwargs["horizontal_speed"]      = 4.0
        kwargs["horizontal_inertia"]    = 20.0
        kwargs["multi_jumps"]           = 2
        kwargs["vertical_acceleration"] = 0.2
        kwargs["jump_velocity"]         = -5.0
        kwargs["fpi"]                   = 4
        kwargs["projectile_class"]      = BB
        kwargs["num_projectiles"]       = 10
        kwargs["hp"]                    = 20
```

All these lines starting with `kwargs` define Fred's characteristics.
The next section looks at them in more detail.
_kwargs_ is short for _keyword arguments_.

```python
        Player.__init__(self, kwargs)
```

Calling the `__init__()` function on `Player` makes Python create a player character with the characteristics just defined in `kwargs`.

```python
        self._c_rect.width = self.rect.width-8
        self._c_rect.centerx = self.rect.centerx
```

This code makes the Fred character a bit narrower than the pictures of Fred.
In the game, if you walk Fred into a wall and look closely, you can see that his gun is actually a few pixels inside the wall.
This code makes that happen.

## Changing Fred

Fred's characteristics can be changed by changing the lines that start with `kwargs[...` in `fred.py`.
For example, the `multi_jumps` key controls how many mid-air jumps a player can make.
When `kwargs["multi_jumps"]` is `2`, then the player can double-jump--the player can jump, and then jump one more time while in the air.
Try changing `multi_jumps` to `3` like this:

```python
        kwargs["multi_jumps"]           = 3
```

Then save fred.py and run the Projectile game.
Fred should now be able to jump twice in mid-air.

The `jump_velocity` key controls how fast Fred moves upward at the start of a jump.
Change `jump_velocity` from `-5.0` to `-10.0`, save `fred.py`, and run the game.
Fred should now jump much higher than before.

Here is a table describing all the keys in `fred.py`.
Try changing them to see what happens.
Remember to save `fred.py` after every change.
Note that some values might make the game act funny or even crash.

| Key | Description |
|-----|-------------|
|`horizontal_speed`| How fast Fred can run |
|`horiztonal_inertia`| How hard it is for Fred to change direction |
|`multi_jumps`| How many consequitive jumps Fred can make without landing |
|`vertical_acceleration`| When jumping, how quickly Fred stops going up and starts coming down |
|`jump_velocity`| How fast Fred moves upward at the start of a jump |
|`fpi`| Animation frames-per-image--how quickly the player animation runs |
|`projectile_class`| What type of projectile Fred uses (note: changing this requires importing the right projectile at the top of `fred.py`) |
|`num_projectiles`| How many projectiles Fred can have in flight at once |
|`hp`| Fred's maximum health (each in-game heart is worth four HP) |


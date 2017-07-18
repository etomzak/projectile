# Projectile

A totally legit pygame game

(But very much in alpha.)

## Installation

### Getting pygame on Linux

See [pygame docs](http://www.pygame.org/wiki/GettingStarted).

### Getting pygame on MacOS

MacOS doesn't have python3 by default. An easy way to get it is with
[Homebrew](https://brew.sh/). From a terminal, install Homebrew:

```
$> /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$> brew update
```

Then install python3:

```
$> brew install python3
```

Then use pip to install pygame:

```
$> pip3 install pygame
```

### Getting Projectile

Clone the game's repository to a suitable location:

```
git clone https://github.com/etomzak/projectile.git projectile_trunk
```

## Running the game

From a terminal:

```
$> cd projectile_trunk
$> ./projectile-game.py
```

A short help page is available with

```
$> ./projectile-game.py -h
```

## Playing the game

Projectile is a simple platformer where you jump around and shoot at stuff.
The game is composed of levels, players, baddies, and projectiles.
You control a player and shoot projectiles at baddies.
Baddies shoot projectiles back at you.
Killing baddies gives you points.
Getting killed by baddies makes you lose the game.
My current personal best for the default, unmodified game is 1490 points.

The game has been designed to make it easy to add new players, baddies, and projectiles.
Support for adding new levels is coming.
Currently there is one level and two each of players, baddies, and projectiles.

### Controls

| Key | Action |
|-----|--------|
|:arrow_left::arrow_right:| Move |
|:arrow_up::arrow_down:   | Look up, look down |
| [space] | Jump  |
| f       | Shoot |
| p       | Pause |
| q       | Quit  |

### Cast

#### Players

| Player | Description |
|--------|-------------|
| ![Fred](/Images/Fred_neutral.png) | **Fred** is your garden-variety stick figure guy. He's trying to get back his gold or rescue the princess or something. Fred starts out with 5 health and shoots BBs by default. |
| ![Ilmar](/Images/Ilmar_stand_straight.png) | **Ilmar** is a tank. He can't be hurt by projectiles, and he shoots slugs by default. Every time he fires, there is a 10% chance that the projectile will backfire and Ilmar will blow up. |

#### Baddies

| Baddie | Description |
|--------|-------------|
| ![Kreutzwald](Images/Kreutzwald.png) | **Kreutzwald** is an angry-looking balloon, but he can't actually hurt you. He has 1 health and is worth 5 points. |
| ![XOR](Images/XOR.png) | **XOR** is an aggressive machine thing that shoots BBs at you as it flies around. It has a small attack surface and is difficult to hit. It has 3 health and is worth 20 points. |

#### Projectiles

| Projectile | Description |
|------------|-------------|
| ![BB](Images/BB.png) | **BB**s are the most basic projectile. They cause 1 damage. A BB power-up has 30 BBs, and normally a player can have 10 BBs in flight at once.
| ![Slug](Images/Slug.png) | **Slug**s are heavy projectiles that do 5 damage. A slug power-up has 10 slugs, and a player can normally have 5 slugs in flight at once. |

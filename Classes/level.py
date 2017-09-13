# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os, random, pygame
from pygame.locals import *

# Add parent directory to path so can get Classes
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.wall import Wall
from Classes.platform import Platform

class Level():
    """"
    Base container class for level backdrops, walls, and platforms.

    Don't instantiate this class; subclass it.

    @param backdrop: Name of 640x480 image for the level background
    @param baddie_classes: List of available Baddies
    @param power_ups: Dictionary of power-ups available to the player
    @param player_projectile_group: Where all Players' fired Projectiles go
    @param decoration_list: Where PSprites that need decorations go

    Barrier attributes:
    floors: prevent characters from moving down; are of type Platform
    ceilings: prevent characters from moving up; are of type Platform
    l_walls: prevent characters from moving right; are of type Wall
    r_walls: prevent characters from moving left; are of type Wall

    Each type of barrier is kept in a pygame.sprite.RenderPlain. While barriers
    can be drawn to the screen, it's assumed that this will only be for
    debugging purposes. The level backdrop should contain all the artwork to
    show a player where barriers are so that the actual Wall and Platform
    objects don't need to be drawn. The level subclass should .add() any
    barriers it needs to floors, ceilings, l_walls, r_walls.

    Character-related attributes:
    player_spawn_x: Player spawn point (x center)
    player_spawn_y: Player spawn point (y center)
    """

    def __init__(self, backdrop, baddie_classes, power_ups=None,
            player_projectile_group=None, decoration_list=None):

    # Set up backdrop
        class_path = os.path.split(os.path.abspath(__file__))[0]
        image_dir = os.path.join(os.path.dirname(class_path), "Images")
        backdrop_f = os.path.join(image_dir, backdrop)

        try:
            self.backdrop = pygame.image.load(backdrop_f)
        except pygame.error:
            print("Cannot load", backdrop_f)
            raise SystemExit

        # Can't imagine why the backdrop would need convert_alpha()
        self.backdrop = self.backdrop.convert()

    # Set up frame of barriers around game area
    # (A subclass can delete these if they're not needed)
        self.floors = pygame.sprite.RenderPlain((Platform(0, 479, 640)))
        self.l_walls = pygame.sprite.RenderPlain((Wall(639, 0, 480)))
        self.r_walls = pygame.sprite.RenderPlain((Wall(0, 0, 480)))
        self.ceilings = pygame.sprite.RenderPlain((Platform(0, 0, 640)))

    # the player and a pygame.sprite.Group containing the Player
        # The group is given to Projectiles and updated by the Level as needed
        self._player_group = pygame.sprite.Group()
        self.player = None
    # Contains Players not currently in play
        self._player_stack = []
    # Group where all Player-fired Projectiles go
        self._player_projectile_group = player_projectile_group
    # Group where all sprite decorations go
        self._decoration_list = decoration_list

    # Default player spawn point
        self.player_spawn_x = 10
        self.player_spawn_y = 10

    # Whether level is over
        self.dead = False

    # Baddies
        # Possible baddies
        self._baddie_classes = baddie_classes
        # Baddies in this level
        self.baddies = pygame.sprite.RenderPlain()
        # Projectiles fired by Baddies
        self.baddie_projectiles = pygame.sprite.RenderPlain()

    # Power-ups
        self._power_up_dict = power_ups
        self._populate_power_up_dict()
        self._power_ups = pygame.sprite.RenderPlain()


    def update(self):
        """
        Generic level logic.
        """

        self.baddies.update()
        self.baddie_projectiles.update()
        self._player_group.update()
        self._player_projectile_group.update()
        if (self.player.dead):
            if len(self._player_stack) > 0:
                centerx = self.player.rect.centerx
                centery = self.player.rect.centery
                # NOTE: If a Projectile fired by a Player hits a baddie after
                #       death, the points won't be counted
                self._pop_player()
                self.player.reset(centerx, centery)
            else:
                self.dead = True


    def clear(self, screen):
        """
        Clear stuff.
        """

        self.baddies.clear(screen, self.backdrop)
        self.baddie_projectiles.clear(screen, self.backdrop)
        self._player_group.clear(screen, self.backdrop)
        self._player_projectile_group.clear(screen, self.backdrop)
        for s in self._decoration_list:
            s.clear_decoration(screen, self.backdrop)


    def draw(self, screen):
        """
        Draw stuff.
        """

        for s in self._decoration_list:
            s.draw_decoration(screen)
        self.baddies.draw(screen)
        self.baddie_projectiles.draw(screen)
        self._power_ups.draw(screen)
        self._player_group.draw(screen)
        self._player_projectile_group.draw(screen)


    def dbg_draw(self, screen):
        """
        Call the draw() function of each barrier class.
        Meant for debugging.
        """

        self.floors.draw(screen)
        self.l_walls.draw(screen)
        self.r_walls.draw(screen)
        self.ceilings.draw(screen)


    def fire(self):
        """
        Tell the primary player to fire.
        """
        self.player.fire()


    def set_player(self, plr):
        """
        Called by the Level owner to set the primary player.
        """

        if len(self._player_group) > 0:
            print("Can't set_player more than once")
            raise SystemExit

        self._player_group.add(plr)
        self.player = plr


    def baddie_killed(self, baddie):
        """
        Signal that a baddie got hit.

        Called by the Baddie that was hit.
        """

        self.baddies.remove(baddie)


    def _populate_power_up_dict(self):
        """
        Make sure self._power_up_dict contains all the necessary fields.
        """

        if self._power_up_dict is None:
            self._power_up_dict = {}

        for key in ['health', 'players', 'projectiles']:
            if key not in self._power_up_dict:
                self._power_up_dict[key] = []


    def _push_player(self, plr):
        """
        Make plr the active player and push current active player onto stack.
        """

        t_plr = self.player
        t_plr.deactivate()
        plr.points = t_plr.points
        self._player_group.remove(t_plr)
        self._player_stack.append(t_plr)
        self._player_group.add(plr)
        self.player = plr


    def _pop_player(self):
        """
        Remove the active player and activate the top player on the stack.
        """

        a_plr = self.player
        self._player_group.remove(a_plr)
        a_plr.deactivate()
        b_plr = self._player_stack.pop()
        b_plr.points = a_plr.points
        b_plr.activate()
        self._player_group.add(b_plr)
        self.player = b_plr


    def _spawn_random_baddie(self, centerx, centery):
        """
        Spawn a random Baddie and add it to baddies.
        """

        i = random.randint(0, len(self._baddie_classes)-1)
        baddie = sorted(self._baddie_classes.keys())[i]

        kwargs = {"owner"             : self,
                  "centerx"           : centerx,
                  "centery"           : centery,
                  "floors"            : self.floors,
                  "l_walls"           : self.l_walls,
                  "r_walls"           : self.r_walls,
                  "ceilings"          : self.ceilings,
                  "fired_projectiles" : self.baddie_projectiles,
                  "targets"           : self._player_group,
                  "decoration_list"   : self._decoration_list}

        self.baddies.add(self._baddie_classes[baddie](kwargs))


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")


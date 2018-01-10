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
from Classes.level import Level
from Classes.character import Character
from Classes.heart import Heart
from Classes.projectileBox import ProjectileBox

class CountdownLevel(Level):
    """
    A type of Level with randomly spawned baddies and power-ups.

    CountdownLevel contains the logic for a simple level with one spawn point
    for baddies and one spawn point for power-ups. The player needs to
    regularly kill baddies to avoid getting hurt by the level.

    Don't instantiate this class; subclass it.

    @param backdrop: Name of 640x480 image for the level background
    @param baddie_classes: A list of available baddies
    @param power_ups: Dictionary of power-ups available to the player
    @param player_projectile_group: Where all Players' fired Projectiles go
    @param decoration_list: Where PSprites that need decorations go
    """

    def __init__(self, backdrop, baddie_classes, power_ups=None,
            player_projectile_group=None, decoration_list=None):

        Level.__init__(self, backdrop, baddie_classes, power_ups,
            player_projectile_group, decoration_list)

    # Baddie variables
        self._baddie_spawn_x = 320 # Should be set in subclass
        self._baddie_spawn_y = 240 # Should be set in subclass

        # Number of frames until next Baddie is spawned
        self._baddie_timer = 120
        # Maximum number of Baddies in the level
        self._max_baddies = 5

    # Player variables
        self.player_spawn_x = 320 # Should be set in subclass
        self.player_spawn_y = 240 # Should be set in subclass

    # Power-up variables
        self._pu_spawn_x = 320 # Should be set in subclass
        self._pu_spawn_y = 240 # Should be set in subclass
        # Number of frames until next possile addition of a power-up
        self._pu_timer = 600
        # Whether a power-up is on-screen
        self._pu_avail = False

    # Hurt timer and display
        # CountdownLevel hurts the player if the player isn't shooting Baddies
        # The amount of time the player has to hit a Baddie is constantly
        #   decreasing to amp up excitement (woot!)

        # Number of frames until player is hurt
        self._hurt_timer = 1800
        # Max value of _hurt_timer
        self._max_hurt_timer = 1800
        # Every 10 frames, _max_hurt_timer is decreased
        self._hurt_dec_timer = 10

        # Hurt timer display
        # Counts down final seconds until Player gets hurt
        if pygame.font:
            font = pygame.font.Font(None, 80)
            self._timer_nums = []
            for i in range(10):
                self._timer_nums.append(font.render(str(i), False, (0, 0, 0)))
            self._timer_rect = self._timer_nums[0].get_rect(centerx = 320,
                                                            centery = 240)


    def update(self):
        """
        All the logic for a CountdownLevel.
        """

        Level.update(self)

    # Possibly throw a power-up into the game
        # Every 10s, there's a 50% chance of a power-up appearing. If the
        #   player hasn't picked up the previous power-up, then the chance is
        #   wasted.
        if self._pu_timer == 0:
            self._pu_timer = 600
            if not self._pu_avail and random.randint(0,1) == 0:
                self._add_pu()
        else:
            self._pu_timer -= 1

    # Add Baddies
        # When the timer hits 0, a random Baddies is added
        if self._baddie_timer != 0:
            self._baddie_timer -= 1
            if self._baddie_timer == 0:
                self._spawn_random_baddie(self._baddie_spawn_x,
                                          self._baddie_spawn_y)

        # Schedule adding a new Baddie in a random number of frames
        if len(self.baddies) < self._max_baddies:
            self._baddie_timer = random.randint(1, 100)

    # Handle picking up power-ups
        # This type of level assumes there's only one power-up in play at a
        #   time. More complex logic is needed if there are more power-ups
        pu = pygame.sprite.spritecollide(self.player, self._power_ups, True)
        if len(pu) > 0:
            print("Power-up caught")
            pu = pu[0]
            pu.disable_box()
            if isinstance(pu, Character):
                self._push_player(pu)
            elif isinstance(pu, Heart):
                self.player.add_hp(pu.hp)
            elif isinstance(pu, ProjectileBox):
                pu.owner = self.player # player may have changed
                self.player.push_box(pu)
            self._pu_avail = False

    # Timers to ensure the Player is killing Baddies
        # If the Player is in a dying animation, the timers aren't changed
        if self.player.hp == 0:
            return

        # Count down to the Player getting hurt
        self._hurt_timer -= 1
        if self._hurt_timer == 0:
            self.player.hurt(1)
            self._hurt_timer = self._max_hurt_timer

        # Reduce maximum amount of time Player has to kill a Baddie
        self._hurt_dec_timer -= 1
        if self._hurt_dec_timer == 0:
            self._hurt_dec_timer = 10
            if self._max_hurt_timer > 300:
                self._max_hurt_timer -= 1
            self._hurt_timer = min(self._hurt_timer, self._max_hurt_timer)


    def clear(self, screen):
        """
        Clear hurt timer display if present.
        """

        if pygame.font:
            if self._hurt_timer < 600:
                screen.blit(self.backdrop, self._timer_rect, self._timer_rect)

        Level.clear(self, screen)


    def draw(self, screen):
        """
        Draw hurt timer if needed.
        """

        if pygame.font:
            if self._hurt_timer < 600:
                screen.blit(self._timer_nums[self._hurt_timer // 60],
                            self._timer_rect)

        Level.draw(self, screen)


    def baddie_killed(self, baddie):
        """
        Signal that a Baddie was killed (death animation might still be
        happening).

        Resets the amount of time the Player has to kill a Baddie.

        Called by the Baddie.
        """

        self._hurt_timer = self._max_hurt_timer


    def _add_pu(self):
        """
        Add a power-up to the level.
        """

        # Which type of power-up to add
        sel = random.randint(0, 2)

        # Heart:
        # TODO: Update for multiple types of health boosts
        if sel == 0:
            pu_kwargs = {"centerx"         : self._pu_spawn_x,
                         "centery"         : self._pu_spawn_y,
                         "decoration_list" : self._decoration_list}
            pu = self._power_up_dict['health'][0](pu_kwargs)
        # Player:
        elif sel == 1:
            length = len(self._power_up_dict['players'])
            if length == 0:
                return
            i = random.randint(0, length-1)
            pu_kwargs = {"owner"             : self,
                         "centerx"           : self._pu_spawn_x,
                         "centery"           : self._pu_spawn_y,
                         "floors"            : self.floors,
                         "l_walls"           : self.l_walls,
                         "r_walls"           : self.r_walls,
                         "ceilings"          : self.ceilings,
                         "targets"           : self.baddies,
                         "fired_projectiles" : self._player_projectile_group,
                         "decoration_list"   : self._decoration_list}
            pu = self._power_up_dict['players'][i](pu_kwargs)
        # Projectile
        else:
            length = len(self._power_up_dict['projectiles'])
            if length == 0:
                return
            i = random.randint(0, length-1)
            pu_kwargs = {"owner"             : self.player,#NOTE: Updated later
                         "floors"            : self.floors,
                         "l_walls"           : self.l_walls,
                         "r_walls"           : self.r_walls,
                         "ceilings"          : self.ceilings,
                         "projectile_class"  : \
                            self._power_up_dict["projectiles"][i],
                         "fired_projectiles" : self._player_projectile_group,
                         "num_projectiles"   : None,
                         "max_shots"         : None,
                         "targets"           : self.baddies,
                         "centerx"           : self._pu_spawn_x,
                         "centery"           : self._pu_spawn_y,
                         "decoration_list"   : self._decoration_list}
            pu = ProjectileBox(pu_kwargs)

        print("Power-up appeared")

        self._power_ups.add(pu)
        self._pu_avail = True
        pu.enable_box()


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")


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
from Classes.wall import Wall
from Classes.platform import Platform
from Classes.character import Character
from Classes.heart import Heart
from Classes.projectileBox import ProjectileBox

class Zero(Level):
    """
    A basic, playable level.

    @param baddie_classes: A list of available baddies
    @param power_ups: Dictionary of power-ups available to the player
    @param player_projectile_group: Where all Players' fired Projectiles go
    """

    def __init__(self, baddie_classes, power_ups=None,
            player_projectile_group=None):

        Level.__init__(self, "Level_Zero.png", baddie_classes, power_ups,
            player_projectile_group)

        # Use barriers provided by Level class, and add some more

        # Bottom u-shaped thick obstacle
        self.floors.add(Platform(36, 448, 568),
                           Platform(32, 416, 4),
                           Platform(604, 416, 4))
        self.ceilings.add(Platform(32, 451, 576))
        self.l_walls.add(Wall(32, 416, 36),
                         Wall(604, 416, 32))
        self.r_walls.add(Wall(35, 416, 32),
                         Wall(607, 416, 36))

        # Two lower _-shaped thick obstacles
        self.floors.add(Platform(1, 384, 63),
                           Platform(576, 384, 63))
        self.ceilings.add(Platform(1, 388, 63),
                          Platform(576, 388, 63))
        self.l_walls.add(Wall(576, 384, 4))
        self.r_walls.add(Wall(63, 384, 4))

        # Two upper _-shaped thick obstacles
        self.floors.add(Platform(64, 32, 192),
                           Platform(384, 32, 192))
        self.ceilings.add(Platform(64, 35, 192),
                          Platform(384, 35, 192))
        self.l_walls.add(Wall(64, 32, 4),
                         Wall(384, 32, 4))
        self.r_walls.add(Wall(255, 32, 4),
                         Wall(575, 32, 4))

        # All the simple landing floors
        self.floors.add(Platform(224, 352, 192),
                           Platform(32, 288, 32),
                           Platform(288, 288, 64),
                           Platform(576, 288, 32),
                           Platform(1, 192, 31),
                           Platform(192, 192, 64),
                           Platform(384, 192, 64),
                           Platform(608, 192, 31),
                           Platform(32, 96, 32),
                           Platform(576, 96, 32))

        # Two one-way walls
        self.l_walls.add(Wall(256, 96, 128))
        self.r_walls.add(Wall(383, 96, 128))

        # The lone ceiling
        self.ceilings.add(Platform(256, 62, 128))

        # Baddie spawn point
        self._baddie_spawn_x = 160
        self._baddie_spawn_y = 128

        self._baddie_timer = 120

        # Center of where player should be spawned at start
        self.player_spawn_x = 18
        self.player_spawn_y = 350

        # Power-up stuff
        self._pu_spawn_x = 480
        self._pu_spawn_y = 128
        self._pu_timer = 600
        self._pu_avail = False

        # Zero hurts the player if the player isn't shooting baddies
        # The amount of time the player has to hit a baddie is constantly
        #   decreasing to amp up excitement (woot!)
        self._hurt_timer = 1800
        self._max_hurt_timer = 1800
        self._hurt_dec_timer = 10

        # Hurt timer display
        # Counts down final 10 seconds until Player gets hurt
        if pygame.font:
            font = pygame.font.Font(None, 80)
            self._timer_nums = []
            for i in range(10):
                self._timer_nums.append(font.render(str(i), False, (0, 0, 0)))
            self._timer_rect = self._timer_nums[0].get_rect(centerx = 320,
                                                            centery = 240)


    def update(self):
        """
        All the logic for this level.
        """

        Level.update(self)

        # Possibly throw a power-up into the game
        if self._pu_timer == 0:
            self._pu_timer = 600
            if not self._pu_avail and random.randint(0,1) == 0:
                self._add_pu()
        else:
            self._pu_timer -= 1

        # Ensure the right number of baddies
        if self._baddie_timer != 0:
            self._baddie_timer -= 1
            if self._baddie_timer == 0:
                self._spawn_random_baddie(self._baddie_spawn_x,
                                          self._baddie_spawn_y)

        if len(self.baddies) < 5:
            self._baddie_timer = random.randint(1, 100)

        # Get collided power-ups
        # This level assumes there's only one power-up in play at a time
        # More complex logic is needed if there are more power-ups
        pu = pygame.sprite.spritecollide(self.player, self._power_ups, True)
        if len(pu) > 0:
            print("Power-up caught")
            pu = pu[0]
            if isinstance(pu, Character):
                self._push_player(pu)
            elif isinstance(pu, Heart):
                self.player.add_hp(pu.hp)
            elif isinstance(pu, ProjectileBox):
                pu.owner = self.player # player may have changed
                self.player.push_box(pu)
            self._pu_avail = False

        # Timers ensure the player is doing something
        # But don't change timers if player is currently croaking
        if self.player.hp == 0:
            return

        self._hurt_timer -= 1
        if self._hurt_timer == 0:
            self.player.hurt(1)
            self._hurt_timer = self._max_hurt_timer

        self._hurt_dec_timer -= 1
        if self._hurt_dec_timer == 0:
            self._hurt_dec_timer = 10
            if self._max_hurt_timer > 300:
                self._max_hurt_timer -= 1
            self._hurt_timer = min(self._hurt_timer, self._max_hurt_timer)


    def clear(self, screen):
        """
        Clear hurt timer display if present before calling class clear().
        """

        if pygame.font:
            if self._hurt_timer < 600:
                screen.blit(self.backdrop, self._timer_rect, self._timer_rect)

        Level.clear(self, screen)


    def draw(self, screen):
        """
        Draw hurt timer if needed before calling class draw().
        """

        if pygame.font:
            if self._hurt_timer < 600:
                screen.blit(self._timer_nums[self._hurt_timer // 60],
                            self._timer_rect)

        Level.draw(self, screen)


    def baddie_killed(self, baddie):
        """
        Signal that a baddie got hit.
        """

        self._hurt_timer = self._max_hurt_timer
        Level.baddie_killed(self, baddie)


    def _add_pu(self):
        """
        Add a power-up to the level.
        """

        if len(self._power_ups) > 1:
            return

        print("Power-up appeared")

        sel = random.randint(0, 2)

        # Heart:
        # TODO: Update for multiple types of health boosts
        if sel == 0:
            pu_kwargs = {"centerx" : self._pu_spawn_x,
                         "centery" : self._pu_spawn_y}
            pu = self._power_up_dict['health'][0](pu_kwargs)
        # Player:
        elif sel == 1:
            length = len(self._power_up_dict['players'])
            if length == 0:
                return
            i = random.randint(0, length-1)
            pu_kwargs = {"centerx"           : self._pu_spawn_x,
                         "centery"           : self._pu_spawn_y,
                         "floors"            : self.floors,
                         "l_walls"           : self.l_walls,
                         "r_walls"           : self.r_walls,
                         "ceilings"          : self.ceilings,
                         "targets"           : self.baddies,
                         "fired_projectiles" : self._player_projectile_group}
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
                         "centery"           : self._pu_spawn_y}
            pu = ProjectileBox(pu_kwargs)

        self._power_ups.add(pu)
        self._pu_avail = True


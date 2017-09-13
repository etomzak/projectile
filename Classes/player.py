# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os, inspect, pygame, time, math
from pygame.locals import *

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.character import Character
from Classes.baddie import Baddie
from Classes.projectileBox import ProjectileBox

class Player(Character):
    """
    Player-controlled character base class.

    Don't instantiate this class; subclass it.

    kwargs must contain:
        floors: pygame.sprite.Group of Platforms that the sprite can stand on
        l_walls: pygame.sprite.Group of Walls that block the sprite moving
                 right
        r_walls: pygame.sprite.Group of Walls that block the sprite moving left
        ceilings: pygame.sprite.Group of Platforms that the sprite is stuck
                  under
        horizontal_speed: Maximum Player speed (pixels per frame)
        horizontal_inertia: Player "weight" (larger is slower acceleration)
        multi_jumps: Max number of consecutive jumps (2 is one mid-air jump)
        vertical_acceleration: How quickly vertical speed changes on a jump
                               (must be >0.0) (smaller values make for longer
                               jumps)
        jump_velocity: Initial speed of jump (must be <0.0) (smaller values
                       make for higher jumps)
        fpi: Frames per image for animation (larger is slower)
        projectile_class: The Projectile class that this Player uses
        num_projectiles: Maximum number of in-flight Projectiles this Player
                         can have
        targets: pygame.sprite.Group of Baddies this Player could hit
        fired_projectiles: pygame.sprite.Group where fired Projectiles go
        ... and whatever is required by Character
    """

    def __init__(self, kwargs):

        Character.__init__(self, kwargs)

        self._populate_images()

        # TODO: Move animation cycling to PSprite?
        self._walk_ctr = 0 # Walk cycle counter
        self._fpi = kwargs["fpi"]
        self._prev_image_series = "none" # Name of previous animation

        self.points = 0

        # Signal that this Player has died
        self.dead = False
        # Number of frames to display dead animation
        self._dead_ctr = 60

        # Platform the player is standing on
        self._floor = None

    # Player control characteristics
        self._max_vx = kwargs["horizontal_speed"]
        self._ix = kwargs["horizontal_inertia"]
        # _mx: current momentum in x-direction
        self._mx = 0.0
        self._j_multi = kwargs["multi_jumps"]
        # _jumps: current number of consecutive jumps without landing
        self._jumps = 0
         # Is SPACE pressed? Don't jump again w/out SPACE being released
         # Defaults to True to prevent jump on spawn
        self._k_space = True
        # Vertical velocity at jump time _j_t is given by
        #   v = _j_a * (_j_t + _j_o) + _j_b
        # _j_t keeps track of how far into a jump the sprite is
        # _j_t == None means that a jump is not in progress
        # _j_o is an offset that ensures that _j_t == 0 is the apogee (useful
        #   for determining speed when falling of floors)
        self._j_a = kwargs["vertical_acceleration"]
        self._j_b = kwargs["jump_velocity"]
        self._j_t = None
        self._j_o = -self._j_b / self._j_a
        # Vertical point direction ((-1, 0, 1) == (down, forward, up))
        self._point_v = 0
        # Horizontal point direction ((-1, 1) == (left, right))
        self._point_h = 1

    # Make sure control characteristics make sense
        if self._max_vx <= 0.0:
            raise ValueError("horizontal_speed must be > 0.0")
        if self._ix <= 0.0:
            raise ValueError("horizontal_inertia must be > 0.0")
        if self._j_multi <= 0:
            raise ValueError("multi_jumps must be > 0")
        if self._j_a <= 0.0:
            raise ValueError("vertical_acceleration must be > 0.0")
        if self._j_b >= 0.0:
            raise ValueError("jump_velocity must be < 0.0")

    # Set targets
        targets = kwargs["targets"]
        if targets is None:
            targets = pygame.sprite.RenderPlain()

    # Set up default Projectile container
        self.fired_projectiles = kwargs["fired_projectiles"]
        b_kwargs = {"owner"             : self,
                    "floors"            : kwargs["floors"],
                    "l_walls"           : kwargs["l_walls"],
                    "r_walls"           : kwargs["r_walls"],
                    "ceilings"          : kwargs["ceilings"],
                    "projectile_class"  : kwargs["projectile_class"],
                    "fired_projectiles" : self.fired_projectiles,
                    "num_projectiles"   : kwargs["num_projectiles"],
                    "max_shots"         : -1,
                    "targets"           : targets,
                    "centerx"           : 0,
                    "centery"           : 0,
                    "decoration_list"   : kwargs["decoration_list"]}
        self._box = ProjectileBox(b_kwargs)

    # Stack of Boxes
        self._box_stack = []

    # Invincibility counter after being hit
        self._invincible_counter = 0

    # Decorations
        # Invincibility
        r = math.ceil(max(self.rect.width, self.rect.height) * 0.75)
        self._dec_invinc_surf = \
            pygame.Surface((r*2, r*2), flags=SRCALPHA).convert_alpha()
        self._dec_invinc_rect = self._dec_invinc_surf.get_rect()
        pygame.draw.circle(self._dec_invinc_surf, (0, 80, 0), (r, r), r-1, 1)
        # Got hit
        self._hit_counter = 0
        self._dec_hit_surf = \
            pygame.Surface((r*2, r*2), flags=SRCALPHA).convert_alpha()
        self._dec_hit_rect = self._dec_invinc_surf.get_rect()
        pygame.draw.circle(self._dec_hit_surf, (255, 0, 0), (r, r), r-1, 0)


    def update(self):
        """
        Update player's state, location, and projectiles.
        """

        if not self.active:
            return

        # Update invincibility
        if self._invincible_counter > 0:
            self._invincible_counter -= 1
            if self._invincible_counter == 0:
                self._decoration_list.remove(self)

        # Hit counter (for hit decoration)
        if self._hit_counter > 0:
            self._hit_counter -= 1
            if self._hit_counter == 0 and self._invincible_counter == 0:
                self._decoration_list.remove(self)

        # If Player is dying, don't do anything else
        if self.hp <= 0 and not self.dead:
            self._dead_ctr -= 1
            if self._dead_ctr == 0:
                self.dead = True
            self._update_image()
            return

        # Get movement from user, update _mx, and calculate change in x and y
        #   coordinates
        dx, dy, self._mx = self._get_movement(self._mx)

        # Motion and collision detection
        # NOTE: The order of these steps DOES matter
        # TODO: All the collision detection assumes that only one barrier can
        #       be hit in a frame. If two barriers of the same type are <dx or
        #       <dy together, the sprite can go through one. A level probably
        #       shouldn't have barriers so close together and sprites moving so
        #       fast. Fix if it becomes a problem.
        # First, check for collisions with walls and update dx accordingly
        # Only required if there is some horizontal motion
        # TODO: Switch to using _basic_obstacle_collision()
        dx = round(dx)
        if dx != 0:
            dx, self._mx = self._check_wall_collision(dx, self._mx)

        # Now that dx is set, test for walking off a floor and possibly
        #   set all required variables to start a jump
        self._check_walk_off(dx)

        # If the player is jumping, calculate dy using jump equation
        if self._j_t is not None:
            dy = self._j_a * (self._j_t + self._j_o) + self._j_b
            self._j_t += 1

        # If the player is somehow in mid-air and not falling (e.g., when
        #   the player is first spawned), set state to jumping
        if self._j_t is None and self._floor is None:
            self._j_t = 0
            self._jumps = 1

        # Check collisions with platforms
        # Only required if there is some vertical motion 
        if dy != 0:
            dy = self._check_platform_collision(dx, dy)

        # Update location
        dy = round(dy)
        self.rect.move_ip(dx, dy)
        self._c_rect.move_ip(dx, dy)

        # Update sprite image
        self._update_image()


    def hit_a_target(self, projectile, target):
        """
        Signal that a Projectile fired by this Player has hit a target.

        This function is called by the Projectile.
        """

        if isinstance(target, Baddie) and target.hp <= 0:
            self.points += target.points


    def got_hit(self, projectile, attacker):
        """
        Signals that the Player got hit by a Projectile.

        Called by the Projectile.
        """

        if not self.active:
            return

        # If invincible, don't get hurt
        if self._invincible_counter > 0:
            return

        print("Character hit")

        if self._hit_counter == 0:
            self._decoration_list.append(self)

        self.hp -= projectile.damage
        self._hit_counter = 5

        if self.hp <= 0:
            print("Character died")
            # The following can only happen if something can damage an
            #   invincible Player
            #if self._invincible_counter > 0:
            #    self._decoration_list.remove(self)
        else:
            self._invincible_counter = 60


    def hurt(self, hp):
        """
        Tell Player it got hurt somehow, but not by a Projectile.

        See also got_hit().
        """

        if not self.active:
            return

        print("Character hurt")

        self.hp -= hp
        if self._invincible_counter == 0 and self._hit_counter == 0:
            self._decoration_list.append(self)
        self._hit_counter = 5

        if self.hp <= 0:
            print("Character died")
        else:
            self._invincible_counter = 60


    def reset(self, centerx=None, centery=None):
        """
        Reset the Player's position and momentum
        """

        if centerx is not None:
            self.rect.centerx = centerx
            self._c_rect.centerx = centerx
        if centery is not None:
            self.rect.centery = centery
            self._c_rect.centery = centery
        self._mx = 0.0
        self._j_t = None
        self._invincible_counter = 60
        self._decoration_list.append(self)


    def push_box(self, box):
        """
        Make box the active ProjectileBox, pushing _box onto a stack.
        """

        self._box_stack.append(self._box)
        self._box = box


    def _pop_box(self):
        """
        Make the acitve ProjectileBox the top Box on the stack.
        """

        try:
            self._box = self._box_stack.pop()
        except IndexError:
            print("Attempted to pop an empty stack")
            # Maybe because default _box._max_shots was non-negative
            raise


    def box_empty(self, box):
        """
        Signal that the currently used ProjectileBox is empty.

        Called by the ProjectileBox.
        """

        print("ProjectileBox empty")
        if self._box is not box:
            print("Attempted to pop wrong box")
            print(" self:", type(self).__name__)
            print(" box :", type(box._owner).__name__)
            raise ValueError

        self._pop_box()


    def fire(self):
        """
        Fire a Projectile.
        """

        if self._box.avail_projectiles() == 0:
            return

        if self.hp <= 0:
            return

        pr = self._box.fire(1)[0]

        direction = 0
        if self._point_v == 1:
            direction = 270
        elif self._point_v == -1:
            direction = 90
        elif self._point_h == -1:
            direction = 180

        pr.reset(centerx = self.rect.centerx, centery = self.rect.centery,
            direction=direction)


    def draw_decoration(self, screen):
        """
        Draw a circle around the Player to indicate being hit.
        """

        if self._hit_counter > 0:
            self._dec_hit_rect.centerx = self.rect.centerx
            self._dec_hit_rect.centery = self.rect.centery
            screen.blit(self._dec_hit_surf, self._dec_hit_rect)
        elif self._invincible_counter > 0:
            self._dec_invinc_rect.centerx = self.rect.centerx
            self._dec_invinc_rect.centery = self.rect.centery
            screen.blit(self._dec_invinc_surf, self._dec_invinc_rect)
        else:
            Character.draw_decoration(self, screen)


    def clear_decoration(self, screen, background):
        """
        Clear circle.
        """

        if self._hit_counter > 0:
            screen.blit(background, self._dec_hit_rect, self._dec_hit_rect)
        elif self._invincible_counter > 0:
            screen.blit(background, self._dec_invinc_rect,
                self._dec_invinc_rect)
        else:
            Character.clear_decoration(self, screen, background)


    def activate(self):
        """
        Bookkeeping to make Player active.
        """
        # TODO: Move this method to Character?

        self.active = True


    def deactivate(self):
        """
        Bookkeeping to make Player inactive.
        """
        # TODO: Move this method to Character?

        self.active = False
        if self._hit_counter > 0 or self._invincible_counter > 0:
            self._decoration_list.remove(self)
            self._hit_counter = 0
            self._invincible_counter = 0


    def _get_movement(self, mx):
        """
        Read the keyboard and figure out maximum player movement.
        """

        # Number of pixels to move player horizontally and vertically
        dx = 0.0
        dy = 0.0

        # Get and handle input
        keys = pygame.key.get_pressed()

        # RIGHT and LEFT adjust momentum, not location, so player can skid
        # Horizontal pointing is always either left or right
        # mx changes by not exactly 1.0 to prevent momentum from becoming
        #   exactly 0.0 while the user is providing input. This prevents the
        #   sprite from going to 'stand' when the player is moving (bit of a
        #   hack).
        if keys[K_RIGHT]:
            mx += 1.0004
            self._point_h = 1
        if keys[K_LEFT]:
            mx -= 1.0005
            self._point_h = -1
        # If neither RIGHT NOR LEFT is pressed, reduce momentum toward 0.0
        if not keys[K_RIGHT] and not keys[K_LEFT]:
            if mx >= 1.0:
                mx -= 1.0
            elif mx <= -1.0:
                mx += 1.0
            elif abs(mx) < 1.0:
                mx = 0.0

        if keys[K_UP]:
            self._point_v = 1
        elif keys[K_DOWN]:
            self._point_v = -1
        else:
            self._point_v = 0

        # Jumping logic
        if keys[K_SPACE]:
            # If the player can jump and SPACE was not pressed during
            #   previous update()
            if self._jumps < self._j_multi and not self._k_space:
                self._jumps += 1
                self._j_t = -self._j_o
                self._k_space = True
                self._floor = None
        else:
            # Set this flag when SPACE is not pressed so next press will
            #   trigger the logic above
            self._k_space = False

        # Adjust dx based on momentum relative to inertia
        # TODO: Maybe allow other things (e.g. spring-loaded walls) to increase
        #   mx above _ix and only cap mx if arrow keys take it above _ix
        if mx > self._ix:
            mx = self._ix
        elif mx < -self._ix:
            mx = -self._ix
        dx += self._max_vx * mx /self._ix

        return dx, dy, mx


    def _check_wall_collision(self, dx, mx):
        """
        Fix dx and _mx values if player is about to go through a wall.
        """

        # Check if running into a left wall
        # Can't run into r_walls if not moving left
        if dx > 0:
            for wall in self.l_walls:
                if self._c_rect.right - 1 <= wall.rect.left and \
                        self._c_rect.right - 1 + dx > wall.rect.left and \
                        self._c_rect.bottom > wall.rect.top and \
                        self._c_rect.top < wall.rect.bottom:
                    dx = wall.rect.left - self._c_rect.right
                    # Almost kill momentum so player is basically stopped
                    #   but keeps running in place
                    mx = 0.1
                    break

        # Check if running into a right wall
        # Can't run into l_walls if not moving left
        if dx < 0:
            for wall in self.r_walls:
                if self._c_rect.left > wall.rect.left and \
                        self._c_rect.left + dx <= wall.rect.left and \
                        self._c_rect.bottom > wall.rect.top and \
                        self._c_rect.top < wall.rect.bottom:
                    dx = wall.rect.left + 1 - self._c_rect.left
                    mx = 0.1
                    break

        return dx, mx


    def _check_walk_off(self, dx):
        """
        Set player to jump if walking off a floor.
        """

        if self._floor:
            if self._floor.rect.right <= self._c_rect.left + dx or \
                    self._floor.rect.left >= self._c_rect.right + dx:
                self._jumps = 1
                self._j_t = 0
                self._floor = None


    def _check_platform_collision(self, dx, dy):
        """
        Fix dy value if it will take the player through a platform.
        """

        # If head-bumping
        # Can only happen if moving up
        if dy < 0:
            for ceiling in self.ceilings:
                if self._c_rect.top >= ceiling.rect.bottom and \
                        self._c_rect.top + dy < ceiling.rect.bottom and \
                        self._c_rect.left + dx < ceiling.rect.right and \
                        self._c_rect.right + dx >= ceiling.rect.left:
                    self._j_t = 0
                    dy = self._c_rect.top - ceiling.rect.bottom
                    break

        # Check if landing on a floor and finish jump if that's the case
        # Can only land when heading down
        if dy > 0:
            for floor in self.floors:
                if self._c_rect.bottom <= floor.rect.top and \
                        self._c_rect.bottom + dy > floor.rect.top and \
                        self._c_rect.left + dx < floor.rect.right and \
                        self._c_rect.right + dx > floor.rect.left:
                    self._floor = floor
                    self._jumps = 0
                    self._j_t = None
                    dy = floor.rect.top - self._c_rect.bottom
                    break

        return dy


    def _populate_images(self):
        """
        Populate missing fields in self._images.

        The Player class assumes a number of poses for the player. This
        function makes sure all those poses at least exist.
        """

        for pos in ['walk', 'stand', 'fly']:
            if pos not in self._images:
                self._images[pos] = {}
            for direction in ['right']:
                if direction not in self._images[pos]:
                    self._images[pos][direction] = {}
                for gaze in ['up', 'straight', 'down']:
                    if gaze not in self._images[pos][direction]:
                        self._images[pos][direction][gaze] = []
                    if not isinstance(self._images[pos][direction][gaze],
                            list) or \
                            len(self._images[pos][direction][gaze]) == 0:
                        self._images[pos][direction][gaze] = [
                        self._images['neutral']
                        ]
            if 'left' not in self._images[pos]:
                self._images[pos]['left'] = {}
            for gaze in ['up', 'straight', 'down']:
                if gaze not in self._images[pos]['left'] or \
                        not isinstance(self._images[pos]['left'][gaze], list):
                    self._images[pos]['left'][gaze] = []
                if len(self._images[pos]['left'][gaze]) == 0:
                    for img in self._images[pos]['right'][gaze]:
                        self._images[pos]['left'][gaze].append(
                            pygame.transform.flip(img, True, False))

        if 'dead' not in self._images:
            self._images['dead'] = [self._images['neutral']]


    def _update_image(self):
        """
        Update image used for sprite based on state at the end of update().
        """

        # Handle dying case
        if self.hp <= 0:
            series = self._images['dead']
        else:
            # Determine position (flying, walking, or standing)
            if self._floor is None:
                series = self._images['fly']
            elif self._mx != 0.0:
                series = self._images['walk']
            else:
                series = self._images['stand']

            # Determine direction (right or left)
            if self._point_h == 1:
                series = series['right']
            else:
                series = series['left']

            # Determine gaze (up, straight, or down)
            if self._point_v == 1:
                series = series['up']
            elif self._point_v == 0:
                series = series['straight']
            else:
                series = series['down']

        if series is not self._prev_image_series:
            self._prev_image_series = series
            self._walk_ctr = 0

        self.image = series[self._walk_ctr // self._fpi]

        # Dying animation freezes on last frame for dramatic effect!!
        if self.hp <= 0:
            if len(series) * self._fpi - 1 > self._walk_ctr:
                self._walk_ctr += 1
        else:
            self._walk_ctr = (self._walk_ctr + 1) % (len(series) * self._fpi)


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")


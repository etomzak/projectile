# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os, inspect, pygame
from pygame.locals import *

class PSprite(pygame.sprite.Sprite):
    """
    Base class for all sprites in the game.

    Provides various utility functions.

    kwargs must contain:
        images: Dictionary pointing to the sprite's image files
        floors: pygame.Group of Platforms that the sprite can stand on
        l_walls: pygame.Group of Walls that block the sprite moving right
        r_walls: pygame.Group of Walls that block the sprite moving left
        ceilings: pygame.Group of Platforms that the sprite is stuck under
        decoration_list: list where any decorations go
    """

    def __init__(self, kwargs):

        pygame.sprite.Sprite.__init__(self)

    # Determine image directory and load images
        # Some sprites might not load images from disk
        if kwargs["images"] is not None:
            class_path = os.path.split(os.path.abspath(__file__))[0]
            self._image_dir = os.path.join(os.path.dirname(class_path),
                "Images")
            self._images = self._string_to_image(kwargs["images"])
        else:
            self._images = None

        # Dummy rect (real one should come from a subclass)
        self.rect = Rect(0,0,0,0)
        # Dummy collision Rect (real one should come from a subclass).
        #   _c_rect is used for testing collisions, and might be offset or
        #   a different size than the drawing Rect.
        self._c_rect = self.rect.copy()

        self.floors = kwargs["floors"]
        self.l_walls = kwargs["l_walls"]
        self.r_walls = kwargs["r_walls"]
        self.ceilings = kwargs["ceilings"]
        self._decoration_list = kwargs["decoration_list"]

    # If barriers (platforms and walls) not given, set to empty
        if self.floors is None:
            self.floors = pygame.sprite.RenderPlain(())
        if self.l_walls is None:
            self.l_walls = pygame.sprite.RenderPlain(())
        if self.r_walls is None:
            self.r_walls = pygame.sprite.RenderPlain(())
        if self.ceilings is None:
            self.ceilings = pygame.sprite.RenderPlain(())

    # Make sure the barriers are of the right type
        if not isinstance(self.floors, pygame.sprite.Group):
            raise TypeError("floors must be a pygame.sprite.Group")
        if not isinstance(self.l_walls, pygame.sprite.Group):
            raise TypeError("l_walls must be a pygame.sprite.Group")
        if not isinstance(self.r_walls, pygame.sprite.Group):
            raise TypeError("r_walls must be a pygame.sprite.Group")
        if not isinstance(self.ceilings, pygame.sprite.Group):
            raise TypeError("ceilings must be a pygame.sprite.Group")


    def _string_to_image(self, obj):
        """
        Replace file name strings with pygame images in a tree-like object.
        """

        if isinstance(obj, str):
            img_path = os.path.join(self._image_dir, obj)
            if not os.path.isfile(img_path):
                print(img_path, "does not exist")
                raise SystemExit
            try:
                temp_img = pygame.image.load(img_path)
            except pygame.error:
                print("Cannot load", img_path)
                raise SystemExit
            obj = temp_img.convert_alpha()

        elif isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = self._string_to_image(obj[i])

        elif isinstance(obj, dict):
            for key in obj.keys():
                obj[key] = self._string_to_image(obj[key])

        return obj


    def _basic_obstacle_collision(self, dx, dy):
        """
        Check if dx or dy will take this sprite into an obstacle.

        Returns (ddx, ddy, obsx, obsy) such that moving the sprite by
        (dx+ddx, dy+ddy) will take the sprite to the edge of any obstacles.
        obsx and obsy are the obstacles the sprite has collided with in the X
        and Y directions.

        Limitations:
        * There is no guaranteed order to barriers, so if barriers are very
        close together, a PSprite might appear to teleport through one to get
        stuck behind the other. This can only happen to very fast-moving
        PSprites and very closely spaced barriers.

        * Collisions in the X and Y directions are calculated independently,
        which can potentially lead to strange results for fast-moving,
        diagonally-moving PSprites.

        The function rounds dx and dy to integers.
        """

        if isinstance(dx, float):
            dx = round(dx)
        if isinstance(dy, float):
            dy = round(dy)

        ddx = 0
        ddy = 0
        obsx = None
        obsy = None

        # If the sprite is moving right
        if dx > 0:
            for wall in self.l_walls:
                if self._c_rect.right - 1 < wall.rect.left and \
                        self._c_rect.right - 1 + dx >= wall.rect.left and \
                        self._c_rect.bottom > wall.rect.top and \
                        self._c_rect.top < wall.rect.bottom:
                    ddx = wall.rect.left - (self._c_rect.right - 1 + dx) - 1
                    obsx = wall
                    break
        # If the sprite is moving left
        elif dx < 0:
            for wall in self.r_walls:
                if self._c_rect.left > wall.rect.left and \
                        self._c_rect.left + dx <= wall.rect.left and \
                        self._c_rect.bottom > wall.rect.top and \
                        self._c_rect.top < wall.rect.bottom:
                    ddx = wall.rect.left - (self._c_rect.left + dx) + 1
                    obsx = wall
                    break

        # If the sprite is moving up
        if dy < 0:
            for platform in self.ceilings:
                if self._c_rect.top > platform.rect.top and \
                        self._c_rect.top + dy <= platform.rect.top and \
                        self._c_rect.right > platform.rect.left and \
                        self._c_rect.left < platform.rect.right:
                    ddy = platform.rect.top - (self._c_rect.top + dy) + 1
                    obsy = platform
                    break
        # If the sprite is moving down
        elif dy > 0:
            for platform in self.floors:
                if self._c_rect.bottom - 1 < platform.rect.top and \
                        self._c_rect.bottom - 1 + dy >= platform.rect.top and \
                        self._c_rect.right > platform.rect.left and \
                        self._c_rect.left < platform.rect.right:
                    ddy = platform.rect.top - (self._c_rect.bottom - 1 + dy) - 1
                    obsy = platform
                    break

        return (ddx, ddy, obsx, obsy)


    def clear(self, screen, background):
        """
        Clear the sprite.

        Feels like pygame should already implement something like this...
        """

        screen.blit(background, self.rect, self.rect)


    def draw(self, screen):
        """
        Blit sprite to screen.
        """

        screen.blit(self.image, self.rect)


    def enable_box(self):
        """
        Turn on black box around PSprite (e.g., when PSprite is a power-up).

        Not done in __init__ because the size of the sprite is not yet
        available there.
        """

        t_rect = self.rect.inflate(4, 4)
        self._dec_box_surf = pygame.Surface((t_rect.width, t_rect.height),
                                flags=SRCALPHA).convert_alpha()
        self._dec_box_rect = self._dec_box_surf.get_rect()
        pygame.draw.rect(self._dec_box_surf, (0, 0, 0),
            pygame.Rect(0, 0, t_rect.width, t_rect.height), 1)

        self._decoration_list.append(self)


    def disable_box(self):
        """
        Turn box off.
        """

        self._decoration_list.remove(self)


    def draw_decoration(self, screen):
        """
        Draw this sprite's box.
        """

        self._dec_box_rect.centerx = self.rect.centerx
        self._dec_box_rect.centery = self.rect.centery
        screen.blit(self._dec_box_surf, self._dec_box_rect)


    def clear_decoration(self, screen, background):
        """
        Clear box.
        """

        screen.blit(background, self._dec_box_rect, self._dec_box_rect)


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")


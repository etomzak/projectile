# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import pygame
from pygame.locals import *

class Platform(pygame.sprite.Sprite):
    """Horizontal barrier

    Platforms can be passed through from the sides and either the top or
    bottom.

    @param left: Left coordinate
    @param top: Top coordinate
    @param width: Width of platform

    (Platform height is always 1.)
    """

    def __init__(self, left, top, width):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(left, top, width, 1)
        self.image = pygame.Surface((self.rect[2], self.rect[3]))
        self.image.fill((0, 255, 0))


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")


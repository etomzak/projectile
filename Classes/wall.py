# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import pygame
from pygame.locals import *

class Wall(pygame.sprite.Sprite):
    """Vertical barrier

    Walls can be passed through from the top, bottom, and one of the sides.

    @param left: Left coordinate
    @param top: Top coordinate
    @param height: height of platform

    (Wall width is always 1.)
    """

    def __init__(self, left, top, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(left, top, 1, height)
        self.image = pygame.Surface((self.rect[2], self.rect[3]))
        self.image.fill((255, 0, 255))


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")


# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import pytest
from pygame.locals import *

"""
pytest unit tests for PSprite.
"""

@pytest.fixture
def boxed_psprite():
    """
    A PSprite inside a box.
    """

    import sys, os, pygame
    # Add parent directory to path so can get Classes
    sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

    from Classes.psprite import PSprite
    from Classes.wall import Wall
    from Classes.platform import Platform

    kwargs = {"images"          : None,
              "floors"          : pygame.sprite.Group(Platform(100, 200, 101)),
              "ceilings"        : pygame.sprite.Group(Platform(100, 100, 101)),
              "l_walls"         : pygame.sprite.Group(Wall(200, 100, 101)),
              "r_walls"         : pygame.sprite.Group(Wall(100, 100, 101)),
              "decoration_list" : None}
    my_sprite = PSprite(kwargs)
    my_sprite._c_rect = Rect(145, 145, 10, 10)
    return my_sprite


@pytest.fixture
def cornered_psprite():
    """
    A PSprite with a nearby corners.
    """

    import sys, os, pygame
    # Add parent directory to path so can get Classes
    sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

    from Classes.psprite import PSprite
    from Classes.wall import Wall
    from Classes.platform import Platform

    kwargs = {"images"          : None,
              "floors"          : pygame.sprite.Group(Platform(100, 190, 11),
                                                      Platform(190, 190, 11)),
              "ceilings"        : pygame.sprite.Group(Platform(100, 110, 11),
                                                      Platform(190, 110, 11)),
              "l_walls"         : pygame.sprite.Group(Wall(190, 100, 11),
                                                      Wall(190, 190, 11)),
              "r_walls"         : pygame.sprite.Group(Wall(110, 100, 11),
                                                      Wall(110, 190, 11)),
              "decoration_list" : None}
    my_sprite = PSprite(kwargs)
    my_sprite._c_rect = Rect(145, 145, 10, 10)
    return my_sprite


def test_no_movement(boxed_psprite):
    (ddx, ddy, obsx, obsy) = boxed_psprite._basic_obstacle_collision(0, 0)
    assert ddx == 0
    assert ddy == 0
    assert obsx is None
    assert obsy is None


def test_move_up_no_collision(boxed_psprite):
    (ddx, ddy, obsx, obsy) = boxed_psprite._basic_obstacle_collision(0, -44)
    assert ddx == 0
    assert ddy == 0
    assert obsx is None
    assert obsy is None


def test_move_down_no_collision(boxed_psprite):
    (ddx, ddy, obsx, obsy) = boxed_psprite._basic_obstacle_collision(0, 45)
    assert ddx == 0
    assert ddy == 0
    assert obsx is None
    assert obsy is None


def test_move_left_no_collision(boxed_psprite):
    (ddx, ddy, obsx, obsy) = boxed_psprite._basic_obstacle_collision(-44, 0)
    assert ddx == 0
    assert ddy == 0
    assert obsx is None
    assert obsy is None


def test_move_right_no_collision(boxed_psprite):
    (ddx, ddy, obsx, obsy) = boxed_psprite._basic_obstacle_collision(45, 0)
    assert ddx == 0
    assert ddy == 0
    assert obsx is None
    assert obsy is None


def test_move_up_collision(boxed_psprite):
    (ddx, ddy, obsx, obsy) = boxed_psprite._basic_obstacle_collision(0, -45)
    assert ddx == 0
    assert ddy == 1
    assert obsx is None
    assert obsy is boxed_psprite.ceilings.sprites()[0]


def test_move_down_collision(boxed_psprite):
    (ddx, ddy, obsx, obsy) = boxed_psprite._basic_obstacle_collision(0, 46)
    assert ddx == 0
    assert ddy == -1
    assert obsx is None
    assert obsy is boxed_psprite.floors.sprites()[0]


def test_move_left_collision(boxed_psprite):
    (ddx, ddy, obsx, obsy) = boxed_psprite._basic_obstacle_collision(-45, 0)
    assert ddx == 1
    assert ddy == 0
    assert obsx is boxed_psprite.r_walls.sprites()[0]
    assert obsy is None


def test_move_right_collision(boxed_psprite):
    (ddx, ddy, obsx, obsy) = boxed_psprite._basic_obstacle_collision(46, 0)
    assert ddx == -1
    assert ddy == 0
    assert obsx is boxed_psprite.l_walls.sprites()[0]
    assert obsy is None


def test_left_collide_down_up(cornered_psprite):
    cornered_psprite._c_rect.left = 120
    cornered_psprite._c_rect.top = 100
    (ddx, _, _, _) = cornered_psprite._basic_obstacle_collision(-20, 0)
    cornered_psprite._c_rect.left += -20 + ddx
    cornered_psprite._c_rect.top += 20
    (ddx, ddy, obsx, obsy) = cornered_psprite._basic_obstacle_collision(0, -20)
    # Check that can jump up
    assert ddx == 0
    assert ddy == 0
    assert obsx is None
    assert obsy is None

    cornered_psprite._c_rect.left -= 1
    (ddx, ddy, obsx, obsy) = cornered_psprite._basic_obstacle_collision(0, -20)
    # Check that can't jump up
    assert ddx == 0
    assert ddy == 11
    assert obsx is None
    assert obsy in cornered_psprite.ceilings.sprites()


def test_right_collide_down_up(cornered_psprite):
    cornered_psprite._c_rect.right = 180
    cornered_psprite._c_rect.top = 100
    (ddx, _, _, _) = cornered_psprite._basic_obstacle_collision(20, 0)
    cornered_psprite._c_rect.right += 20 + ddx
    cornered_psprite._c_rect.top += 20
    (ddx, ddy, obsx, obsy) = cornered_psprite._basic_obstacle_collision(0, -20)
    # Check that can jump up
    assert ddx == 0
    assert ddy == 0
    assert obsx is None
    assert obsy is None

    cornered_psprite._c_rect.right += 1
    (ddx, ddy, obsx, obsy) = cornered_psprite._basic_obstacle_collision(0, -20)
    # Check that can't jump up
    assert ddx == 0
    assert ddy == 11
    assert obsx is None
    assert obsy in cornered_psprite.ceilings.sprites()


def test_left_collide_up_down(cornered_psprite):
    cornered_psprite._c_rect.left = 120
    cornered_psprite._c_rect.top = 190
    (ddx, _, _, _) = cornered_psprite._basic_obstacle_collision(-20, 0)
    cornered_psprite._c_rect.left += -20 + ddx
    cornered_psprite._c_rect.top -= 20
    (ddx, ddy, obsx, obsy) = cornered_psprite._basic_obstacle_collision(0, 20)
    # Check that can fall past floor
    assert ddx == 0
    assert ddy == 0
    assert obsx is None
    assert obsy is None

    cornered_psprite._c_rect.left -= 1
    (ddx, ddy, obsx, obsy) = cornered_psprite._basic_obstacle_collision(0, 20)
    # Check that will land
    assert ddx == 0
    assert ddy == -10
    assert obsx is None
    assert obsy in cornered_psprite.floors.sprites()


def test_right_collide_up_down(cornered_psprite):
    cornered_psprite._c_rect.right = 180
    cornered_psprite._c_rect.top = 190
    (ddx, _, _, _) = cornered_psprite._basic_obstacle_collision(20, 0)
    cornered_psprite._c_rect.left += 20 + ddx
    cornered_psprite._c_rect.top -= 20
    (ddx, ddy, obsx, obsy) = cornered_psprite._basic_obstacle_collision(0, 20)
    # Check that can fall past floor
    assert ddx == 0
    assert ddy == 0
    assert obsx is None
    assert obsy is None

    cornered_psprite._c_rect.right += 1
    (ddx, ddy, obsx, obsy) = cornered_psprite._basic_obstacle_collision(0, 20)
    # Check that will land
    assert ddx == 0
    assert ddy == -10
    assert obsx is None
    assert obsy in cornered_psprite.floors.sprites()



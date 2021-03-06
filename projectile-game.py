#! /usr/bin/env python3

# projectile-game.py -- A pygame platformer
# Copyright (C) 2017  Erik Tomusk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os, inspect, importlib, time, random
import pygame
from optparse import OptionParser
from pygame.locals import *
from Classes.character import Character
from Classes.player import Player
from Classes.baddie import Baddie
from Classes.countdownLevel import CountdownLevel
from Classes.heart import Heart
from Levels.zero import Zero
from Classes.projectile import Projectile

# Some global variables for the game
GAME_DIR = os.path.split(os.path.abspath(__file__))[0]

def main():
# User input
    OPT = get_options()

# Find and load game assets
    player_classes = get_subclasses("Characters", Player)
    baddie_classes = get_subclasses("Baddies", Baddie)
    projectile_classes = get_subclasses("Projectiles", Projectile)
    # TODO: This needs to be extended when other types of levels become
    #   available
    level_classes = get_subclasses("Levels", CountdownLevel)

# Determine the main player character
    # Happens before asset exclusion below to allow complete configuration to
    #   be printed
    primary_player_classname = OPT.player
    if primary_player_classname is None:
        # Fred is the game's default
        if "Fred" in OPT.exclude:
            players = []
            for player in sorted(player_classes.keys()):
                if player not in OPT.exclude:
                    players.append(player)
            if len(players) == 0:
                print("ERROR: No players available")
                raise SystemExit
            i = random.randint(0, len(players)-1)
            primary_player_classname = players[i]
        else:
            primary_player_classname = "Fred"

    if primary_player_classname not in player_classes:
        print("Error: I don't know any " + primary_player_classname)
        raise SystemExit

# Print game configuration
    print("Found players:")
    for player in sorted(player_classes.keys()):
        if player == primary_player_classname:
            print("* " + player)
        elif player in OPT.exclude:
            print("- " + player)
        else:
            print("+ " + player)

    print("Found baddies:")
    for baddie in sorted(baddie_classes.keys()):
        if baddie in OPT.exclude:
            print("- " + baddie)
        else:
            print("+ " + baddie)

    print("Found projectiles:")
    for pr in sorted(projectile_classes.keys()):
        if pr in OPT.exclude:
            print("- " + pr)
        else:
            print("+ " + pr)

    print("Found Levels:")
    for level in sorted(level_classes.keys()):
        if level in OPT.exclude:
            print("- " + level)
        else:
            print("+ " + level)

# Print quick instructions
    print("\nControls:")
    print("Arrows: Move")
    print("Space:  Jump")
    print("f:      Fire")
    print("p:      Pause")
    print("q:      Quit\n")

# Remove excluded assets
    for item in OPT.exclude:
        baddie_classes.pop(item, None)
        player_classes.pop(item, None)
        projectile_classes.pop(item, None)
        level_classes.pop(item, None)

# Check that there is a level
    if len(level_classes) == 0:
        print("ERROR: No levels available")
        raise SystemExit

# Dictionary of available power-ups that a Level can use
    power_ups = {'players': [],
                 'projectiles': list(projectile_classes.values()),
                 'health': [Heart]}
    for player in sorted(player_classes.keys()):
        if player != primary_player_classname:
            power_ups['players'].append(player_classes[player])

# Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Projectile")
    pygame.mouse.set_visible(0)
    try:
        icon = pygame.image.load(os.path.join(GAME_DIR, "Images", "icon.png"))
    except pygame.error:
        print("Cannot load icon.png")
        raise SystemExit
    pygame.display.set_icon(icon)

    # All Projectiles fired by all players end up here
    player_projectile_group = pygame.sprite.RenderPlain()
    # PSprites that want decorations place themselves here
    decoration_list = []

    # The Level object
    # Most everything happens through the Level
    level_name = OPT.level
    if level_name is None:
        i = random.randint(0, len(level_classes)-1)
        level_name = sorted(level_classes.keys())[i]

    if level_name not in level_classes:
        print("Error: I don't know any " + level_name)
        raise SystemExit

    a_level = level_classes[level_name](
        baddie_classes,
        power_ups,
        player_projectile_group,
        decoration_list)
    screen.blit(a_level.backdrop, (0, 0))

    # The main Player object
    # Game over when a_dude dies
    p_kwargs = {"owner"             : a_level,
                "centerx"           : a_level.player_spawn_x,
                "centery"           : a_level.player_spawn_y,
                "floors"            : a_level.floors,
                "l_walls"           : a_level.l_walls,
                "r_walls"           : a_level.r_walls,
                "ceilings"          : a_level.ceilings,
                "targets"           : a_level.baddies,
                "fired_projectiles" : player_projectile_group,
                "decoration_list"   : decoration_list}
    a_dude = player_classes[primary_player_classname](p_kwargs)

    a_level.set_player(a_dude)

    clock = pygame.time.Clock()

# Score display
    score = 0
    if pygame.font:
        font = pygame.font.Font(None, 20)
        score_text = font.render(str(score), False, (0, 0, 0))
        score_rect = score_text.get_rect(top=2, right=598)

        screen.blit(score_text, score_rect)

# Health display
    health = a_dude.hp

    hearts = []

    for name in ["heart_1.png", "heart_2.png", "heart_3.png", "heart_4.png"]:
        try:
            heart = pygame.image.load(os.path.join(GAME_DIR, "Images", name))
        except pygame.error:
            print("Cannot load", name)
            raise SystemExit
        heart = heart.convert_alpha()
        hearts.append(heart)

    heart_rect = hearts[3].get_rect()
    heart_area = Rect(3, 2, 90, 15)

    pygame.display.flip()

# Ammo count
    if pygame.font:
        ammo_count = 0
        prev_ammo_count = 0
        ammo_class = None
        prev_ammo_class = None
        ammo_img_surf = None
        ammo_img_rect = None
        ammo_img_area = pygame.Rect(600, 2, 22, 16)
        ammo_count_text = []
        for i in range(100):
            ammo_count_text.append(font.render(str(i).zfill(2), False,
                (0, 0, 0)))

        # "02" is the widest ammo display at 16 pixels
        ammo_count_area = ammo_count_text[2].get_rect(top=2, right=637)

# FPS display
    if OPT.fps and pygame.font:
        fps_text = font.render("00", False, (0, 0, 0))
        fps_rect = fps_text.get_rect(bottom=478, right=637)

# Game Over display
    game_over = pygame.Surface((640, 480), flags = SRCALPHA)
    game_over.fill((180, 180, 180, 192))
    if pygame.font:
        go_font = pygame.font.Font(None, 80)
        go_text = go_font.render("Game Over", False, (0, 0, 0))
        go_rect = go_text.get_rect(centerx=320, centery=240)
        game_over.blit(go_text, go_rect)

# Pause flag and display
    pause_flag = False
    prev_pause_flag = False
    pause = pygame.Surface((640, 480), flags = SRCALPHA)
    pause.fill((180, 180, 180, 192))
    if pygame.font:
        pause_font = pygame.font.Font(None, 80)
        pause_text = pause_font.render("Pause", False, (0, 0, 0))
        pause_rect = pause_text.get_rect(centerx=320, centery=240)
        pause.blit(pause_text, pause_rect)

# Main game loop
    while 1:
        clock.tick(60)

        prev_pause_flag = pause_flag

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_f:
                    a_level.fire()
                elif (event.key == K_ESCAPE or event.key == K_q):
                    sys.exit()
                elif event.key == K_p:
                    pause_flag = not pause_flag

    # Game pausing
        if pause_flag:
            if not prev_pause_flag:
                screen.blit(pause, (0, 0))
                pygame.display.flip()
            continue
        if not pause_flag and prev_pause_flag:
            screen.blit(a_level.backdrop, (0, 0))

    # Clear and update
        a_level.clear(screen)
        a_level.update()

    # Clear health area if needed
        if health != a_level.player.hp:
            screen.blit(a_level.backdrop, heart_area, heart_area)
            health = a_level.player.hp

    # Draw various text
        if pygame.font:

    # Draw score
            if a_level.points != score:
                screen.blit(a_level.backdrop, score_rect, score_rect)
                score = a_level.points
                score_text = font.render(str(score), False, (0, 0, 0))
                score_rect = score_text.get_rect(top=2, right=598)

            screen.blit(score_text, score_rect)

    # Draw ammo count
            if a_level.player._box._max_shots == -1:
                ammo_count = 99
            else:
                ammo_count = a_level.player._box._max_shots - \
                    a_level.player._box._shots_fired

            ammo_class = a_level.player._box.projectile_class
            if ammo_class is not prev_ammo_class:
                prev_ammo_class = ammo_class
                ammo_img_surf = a_level.player._box.unused_projectiles.\
                    sprites()[0].image.copy()
                ammo_img_rect = ammo_img_surf.get_rect(centerx=611, centery=8)
                screen.blit(a_level.backdrop, ammo_img_area, ammo_img_area)

            if ammo_count != prev_ammo_count:
                screen.blit(a_level.backdrop, ammo_count_area, ammo_count_area)
                prev_ammo_count = ammo_count

            screen.blit(ammo_count_text[ammo_count], ammo_count_area)
            screen.blit(ammo_img_surf, ammo_img_rect)

    # Draw FPS
            if OPT.fps:
                screen.blit(a_level.backdrop, fps_rect, fps_rect)
                fps = int(clock.get_fps())
                fps_text = font.render(str(fps), False, (0, 0, 0))
                fps_rect = fps_text.get_rect(bottom=478, right=637)
                screen.blit(fps_text, fps_rect)

    # Draw health
        full_hearts = health // 4
        frac_hearts = health % 4

        for i in range(full_hearts):
            screen.blit(hearts[3], (i*18+3, 2))
        if frac_hearts == 1:
            screen.blit(hearts[0], (full_hearts*18+3, 2))
        elif frac_hearts == 2:
            screen.blit(hearts[1], (full_hearts*18+3, 2))
        elif frac_hearts == 3:
            screen.blit(hearts[2], (full_hearts*18+3, 2))

    # Draw everything else
        a_level.draw(screen)

    # Flip
        pygame.display.flip()

    # On death:
        if a_level.dead:
            break

# Game over
    screen.blit(game_over, (0,0))
    if pygame.font:
        final_score_font = pygame.font.Font(None, 60)
        score_text = final_score_font.render("Final score: " + str(score),
            False, (1, 0, 0))
        score_rect = score_text.get_rect(centerx=320, top=280)
        screen.blit(score_text, score_rect)


    pygame.display.flip()

# Gamve over loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q or \
                        event.key == K_RETURN:
                    sys.exit()


def get_subclasses(directory, base):
    """
    Get subclasses of a base class from all Python files in a directory.

    For this function, a class is NOT its own subclass (unlike what the
    built-in issubclass() function thinks).
    directory is assumed to be in GAME_DIR. Further nesting is not supported.

    Inspired in part by https://code.activestate.com/recipes/553262-list-
    classes-methods-and-functions-in-a-module/.
    """

    if not os.path.isdir(os.path.join(GAME_DIR, directory)):
        print(directory, "does not exist")
        raise SystemExit

    # Get list of python modules
    pys = []
    for f in os.listdir(directory):
        if f.endswith(".py"):
            pys.append(directory + "." + f.replace(".py", ""))

    # Import all the modules and find the correct classes
    classes = {}
    for py in pys:
        t_mod = importlib.import_module(py)
        for item in dir(t_mod):
            obj = getattr(t_mod, item)
            if inspect.isclass(obj) and \
                    issubclass(obj, base) and \
                    obj is not base:
                classes[obj.__name__] = obj

    return classes


def get_options():
    """
    Parse command line options.
    """

    parser = OptionParser()

    parser.add_option("-p", "--player", action="store", type="string",
        dest="player", default=None, help="Select default player character")

    parser.add_option("-l", "--level", action="store", type="string",
        dest="level", default=None, help="Select level to play on")

    parser.add_option("-n", "--not", action="append", type="string",
        dest="exclude", default=[],
        help="Characters, baddies, projectiles, and levels to exclude")

    parser.add_option("--fps", action="store_true", dest="fps", default=False,
        help="Show game's FPS")

    (OPT, _) = parser.parse_args()

    if OPT.player in OPT.exclude:
        parser.error("Player given with --player then excluded with --not")

    if OPT.level in OPT.exclude:
        parser.error("Level given with --level then excluded with --not")

    return OPT


if __name__ == "__main__":
    main()


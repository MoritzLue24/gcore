import pygame
from . import camera
from . import get_cfg


def screen_pos(game_pos: pygame.Vector2):
    return pygame.Vector2(
        game_pos.x * get_cfg("tile_size")[0],
        game_pos.y * get_cfg("tile_size")[1]
    ) * get_cfg("scale") / 10 + camera.offset()

def game_pos(screen_pos: pygame.Vector2):
    a = (screen_pos - camera.offset()) / get_cfg("scale") * 10
    return pygame.Vector2(
        a.x / get_cfg("tile_size")[0],
        a.y / get_cfg("tile_size")[1]
    )

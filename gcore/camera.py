import pygame
from .config import get_cfg


__pos = pygame.Vector2(0, 0)

def set_pos(pos: pygame.Vector2):
    global __pos
    __pos = pos

def offset() -> pygame.Vector2:
    #return pygame.Vector2(0, 0)
    real_pos = pygame.Vector2(
        __pos.x * get_cfg("tile_size")[0],
        __pos.y * get_cfg("tile_size")[1]
    ) * get_cfg("scale") / 10
    return pygame.Vector2(pygame.display.get_window_size()) // 2 - real_pos

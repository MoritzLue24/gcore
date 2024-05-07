import pygame
from . import image
from . import ui
from .config import set_cfg, append_cfg, get_cfg
from .animation import Animation
from .entity import Entity
from .tiles import load_tileset, Tilemap
from . import camera


def update_all():
    for entity in Entity.instances:
        entity.update()

def draw_all(surface):
    for entity in Entity.instances:
        entity.draw(surface)
    ui.Dialogue.draw(surface)

def screen_pos(game_pos: pygame.Vector2):
    return pygame.Vector2(
        game_pos.x * get_cfg("tile_size")[0],
        game_pos.y * get_cfg("tile_size")[1]
    ) * get_cfg("scale") + camera.offset()

def game_pos(screen_pos: pygame.Vector2):
    a = (screen_pos - camera.offset()) / get_cfg("scale")
    return pygame.Vector2(
        a.x / get_cfg("tile_size")[0],
        a.y / get_cfg("tile_size")[1]
    )

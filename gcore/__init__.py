import pygame
from . import image
from . import ui
from .config import set_cfg, append_cfg, get_cfg
from .animation import Animation
from .pos import screen_pos, game_pos
from .entity import Entity
from .tiles import load_tileset, Tilemap
from . import camera


def update_all():
    for entity in Entity.instances:
        entity.update()

def draw_all(surface):
    if Tilemap.active:
        Tilemap.active.draw(surface)
    for entity in Entity.instances:
        entity.draw(surface)
    for panel in ui.Panel.instances:
        panel.draw(surface)
    ui.Dialogue.draw(surface)


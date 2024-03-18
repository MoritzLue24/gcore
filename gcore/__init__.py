from . import image
from . import ui
from .config import set_cfg, append_cfg, get_cfg
from .animation import Animation
from .entity import Entity
from .item import Item


def update_all():
    for entity in Entity.instances:
        entity.update()

def draw_all(surface):
    for entity in Entity.instances:
        entity.draw(surface)
    ui.Dialogue.draw(surface)


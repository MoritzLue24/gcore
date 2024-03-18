from . import image
from . import ui
from .config import set_cfg, append_cfg, get_cfg
from .animation import Animation
from .entity import Entity
from .item import Item


def update_all():
    Entity.update()
    Item.update()

def draw_all(surface):
    Entity.draw(surface)
    Item.draw(surface)
    ui.Dialogue.draw(surface)


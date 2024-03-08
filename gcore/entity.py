import pygame

from .animation import Animation


class Entity:
    instances = []
    def __init__(
        self,
        pos: pygame.Vector2,
        animations: dict[str, Animation],
        init_state: str
    ):
        self.pos = pos
        self.animations = animations
        self.init_state = init_state
        self.state = init_state
        
        Entity.instances.append(self)

    @staticmethod
    def update():
        for entity in Entity.instances:
            for state, animation in entity.animations.items():
                if state == entity.state:
                    animation.update()
                    if animation.is_finished():
                        animation.reset()
                        entity.state = entity.init_state
                else:
                    animation.reset()

    @staticmethod
    def draw(surface: pygame.Surface):
        for entity in Entity.instances:
            surface.blit(entity.animations[entity.state].current(), entity.pos)

    def delete(self):
        Entity.instances.remove(self)



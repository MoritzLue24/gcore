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

        self.__flipped = (False, False)
        
        Entity.instances.append(self)

    def set_flipped(self, vertical: bool, horizontal: bool):
        for anim in self.animations.values():
            for i, frame in enumerate(anim.frames):
                anim.frames[i] = pygame.transform.flip(
                    frame,
                    self.__flipped[0] != vertical,
                    self.__flipped[1] != horizontal
                )
        self.__flipped = (vertical, horizontal)

    def get_flipped(self) -> tuple[bool, bool]:
        return self.__flipped

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



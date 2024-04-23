import pygame
from .animation import Animation
from . import camera


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
        self.state = init_state

        self.__init_state = init_state
        self.__flipped = (False, False)
        
        Entity.instances.append(self)

    def set_flipped(self, flip_x: bool, flip_y: bool):
        for anim in self.animations.values():
            for i, frame in enumerate(anim.frames):
                anim.frames[i] = pygame.transform.flip(
                    frame,
                    self.__flipped[0] != flip_x,
                    self.__flipped[1] != flip_y
                )
        self.__flipped = (flip_x, flip_y)

    def get_flipped(self) -> tuple[bool, bool]:
        return self.__flipped

    def update(self):
        for state, anim in self.animations.items():
            if state == self.state:
                anim.update()
                if anim.is_finished():
                    anim.reset()
                    self.state = self.__init_state
            else:
                anim.reset()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.animations[self.state].current(), self.pos + camera.offset())

    def delete(self):
        Entity.instances.remove(self)

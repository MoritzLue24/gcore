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

    def update(self):
        for state, animation in self.animations.items():
            if state == self.state:
                animation.update()
                if animation.is_finished():
                    animation.reset()
                    self.state = self.init_state
            else:
                animation.reset()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.animations[self.state].current(), self.pos)

    def delete(self):
        Entity.instances.remove(self)



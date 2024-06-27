import pygame
import math
from .animation import Animation
from .tiles import Tilemap
from .config import get_cfg
from . import camera
from .pos import screen_pos


class Entity:
    instances = []
    def __init__(
        self,
        pos: pygame.Vector2,
        animations: dict[str, Animation],
        init_state: str,
        hitbox_size: pygame.Vector2
    ):
        self.pos = pos
        self.animations = animations
        self.state = init_state
        self.hitbox_size = hitbox_size

        self.__init_state = init_state
        self.__flipped = (False, False)
        
        Entity.instances.append(self)

    def move(self, dir: pygame.Vector2):
        dir = pygame.Vector2(int(dir.x), int(dir.y))
        if Tilemap.active == None: raise ValueError("cannot move without tilemap")
        if dir.magnitude() == 0: return

        # get point of collision `emit_point` between `rect` and self.pos + dir.
        # then, get the Tilemap collision point from `emit_point` + dir
        # FIXME: for some reason diagonal dirs do not work, only straight

        rect = pygame.Rect(
            self.pos.x - self.hitbox_size.x / 2,
            self.pos.y - self.hitbox_size.y / 2,
            self.hitbox_size.x,
            self.hitbox_size.y
        )
        border_cols = []
        sides = [
            (pygame.Vector2(rect.x, rect.y), pygame.Vector2(rect.w, 0)),
            (pygame.Vector2(rect.x, rect.y), pygame.Vector2(0, rect.h)),
            (pygame.Vector2(rect.x + rect.w, rect.y), pygame.Vector2(0, rect.h)),
            (pygame.Vector2(rect.x, rect.y + rect.h), pygame.Vector2(rect.w, 0))
        ]
        for side in sides:
            x1, y1 = self.pos
            x2, y2 = self.pos + dir
            x3, y3 = side[0]
            x4, y4 = side[0] + side[1]

            slope1 = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
            slope2 = (y4 - y3) / (x4 - x3) if x4 - x3 != 0 else float('inf')
            if slope1 == slope2: continue
            
            intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) *
                (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) *
                (x3 - x4))
            intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) *
                (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) *
                (x3 - x4))
            intersection = pygame.Vector2(intersection_x, intersection_y)

            # check if intersection point lies within the range of the hitbox rect
            col_x2 = min(x3, x4) <= intersection_x <= max(x3, x4)
            col_y2 = min(y3, y4) <= intersection_y <= max(y3, y4)

            if col_x2 and col_y2:
                border_cols.append(pygame.Vector2(intersection_x, intersection_y))

        border_cols.sort(key=lambda x: (x - (self.pos + dir)).magnitude())
        emit_point = border_cols[0]

        (col_point, _) = Tilemap.active.collision_point(emit_point, dir)

        emit_diff = emit_point - self.pos
        self.pos = col_point - emit_diff

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
        if Tilemap.active == None: raise ValueError("cannot draw without tilemap")
        image_offset = pygame.Vector2(self.animations[self.state].current().get_size()) / 2
        surface.blit(
            self.animations[self.state].current(),
            screen_pos(self.pos) - image_offset
        )
        pygame.draw.circle(surface, (255, 255, 255), screen_pos(self.pos), 7)

    def delete(self):
        Entity.instances.remove(self)

import pygame
from .animation import Animation
from .tiles import Tilemap
from .pos import screen_pos
from .utils import line_intersection, LinesAreParallel


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

    def move_ccd(self, dir: pygame.Vector2):
        """move this entity and avoid tunneling (ccd)"""
        if Tilemap.active == None: raise ValueError("cannot move without tilemap")
        dir = pygame.Vector2(int(dir.x), int(dir.y))
        if dir.magnitude() == 0: return

        # get point of collision `emit_point` between `rect` and self.pos + dir.
        # then, get the Tilemap collision point from `emit_point` + dir
        # FIXME: for some reason diagonal dirs do not work, only straight
        # FIXME: use different approach: 
        #   (now, it only works from a line on self.pos.y. every tile below that is ignored)
        #   1. copyshift the hitbox rect along dir and check for rect-to-rect collision
        #   2. use multiple lines exept jsut the pos + dir line. (from hitbox corners)
        #   3. raycasting (inefficient)
        rect = pygame.Rect(
            self.pos.x - self.hitbox_size.x / 2,
            self.pos.y - self.hitbox_size.y / 2,
            self.hitbox_size.x,
            self.hitbox_size.y
        )
        sides = [
            (pygame.Vector2(rect.x, rect.y), pygame.Vector2(rect.w, 0)),
            (pygame.Vector2(rect.x, rect.y), pygame.Vector2(0, rect.h)),
            (pygame.Vector2(rect.x + rect.w, rect.y), pygame.Vector2(0, rect.h)),
            (pygame.Vector2(rect.x, rect.y + rect.h), pygame.Vector2(rect.w, 0))
        ]
        border_cols = []
        for side in sides:
            try:
                intersection, _ = line_intersection(self.pos, dir, side[0], side[1])
                border_cols.append(intersection)
            except LinesAreParallel:
                continue

        border_cols.sort(key=lambda x: (x - (self.pos + dir)).magnitude())
        emit_point = border_cols[0]

        (col_point, _) = Tilemap.active.collision_point(emit_point, dir)
        emit_diff = emit_point - self.pos
        self.pos = col_point - emit_diff
    
    def move(self, dir: pygame.Vector2):
        if Tilemap.active == None: raise ValueError("cannot move without tilemap")
        dir = pygame.Vector2(int(dir.x), int(dir.y))
        rect = pygame.Rect(
            self.pos.x - self.hitbox_size.x / 2 + dir.x,
            self.pos.y - self.hitbox_size.y / 2 + dir.y,
            self.hitbox_size.x,
            self.hitbox_size.y
        )
        if not Tilemap.active.collide_rect(rect):
            self.pos += dir

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
        # pygame.draw.circle(surface, (255, 255, 255), screen_pos(self.pos), 7)

    def delete(self):
        Entity.instances.remove(self)

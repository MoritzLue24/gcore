import time
import pygame
from . import image
from .config import get_cfg


class Animation:
    def __init__(
        self,
        frames: list[pygame.Surface],
        fps: float,
        looping: bool
    ):
        self.frames = [
            pygame.transform.scale_by(frame, get_cfg("scale"))
            for frame in frames
            if not image.is_empty(frame)
        ]
        self.fps = fps
        self.looping = looping
        
        self.i = 0
        self.paused = False

        self.__start_time = time.time()
        self.__finished = False
        self.__flipped = (False, False)

    def is_finished(self) -> bool:
        return self.__finished

    def set_flip(self, vertical: bool, horizontal: bool):
        for i, frame in enumerate(self.frames):
            self.frames[i] = pygame.transform.flip(
                frame,
                self.__flipped[0] != vertical,
                self.__flipped[1] != horizontal
            )
        self.__flipped = (vertical, horizontal)

    def update(self):
        if self.__finished or self.paused:
            return

        if self.i >= len(self.frames) - 1:
            if self.looping: self.i = 0
            else: self.__finished = True
            return

        current_time = time.time()
        if current_time - self.__start_time >= 1.0 / self.fps:
            self.__start_time = current_time
            self.i += 1

    def reset(self):
        """this does not affect if the frames are flipped"""
        self.i = 0
        self.paused = False
        self.__start_time = time.time()
        self.__finished = False

    def current(self) -> pygame.Surface:
        return self.frames[self.i]

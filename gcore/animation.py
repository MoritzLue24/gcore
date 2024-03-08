import time
import pygame
from . import image


class Animation:
    def __init__(
        self,
        frames: list[pygame.Surface],
        fps: float,
        looping: bool
    ):
        self.frames = [frame for frame in frames if not image.is_empty(frame)]
        self.fps = fps
        self.looping = looping
        
        self.i = 0
        self.paused = False

        self.__start_time = time.time()
        self.__finished = False

    def is_finished(self) -> bool:
        return self.__finished

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
        self.i = 0
        self.paused = False
        self.__start_time = time.time()
        self.__finished = False

    def current(self) -> pygame.Surface:
        return self.frames[self.i]

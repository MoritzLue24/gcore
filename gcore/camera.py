import pygame


__pos = pygame.Vector2(0, 0)

def set_pos(pos: pygame.Vector2):
    global __pos
    __pos = pos

def offset() -> pygame.Vector2:
    return pygame.Vector2(pygame.display.get_window_size()) // 2 - __pos

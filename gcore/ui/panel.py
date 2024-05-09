import pygame
from . import fonts
from ..config import get_cfg


class Panel:
    instances = []
    def __init__(self, rect: pygame.Rect, texts: list[str]):
        self.rect = rect
        self.__text_surfs = [
            fonts["text"].render(text, False, (255, 255, 255))
            for text in texts
        ]
        Panel.instances.append(self)
    
    def set_text(self, i, text: str):
        self.__text_surfs[i] = fonts["text"].render(
            text, False, (255, 255, 255)
        )

    def draw(self, surface: pygame.Surface):
        inner_rect = pygame.Rect(
            self.rect.x + get_cfg("panel_border_width"),
            self.rect.y + get_cfg("panel_border_width"),
            self.rect.width - 2 * get_cfg("panel_border_width"),
            self.rect.height - 2 * get_cfg("panel_border_width")
        )
        rect_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            rect_surf,
            get_cfg("panel_border_color"),
            (0, 0, self.rect.w, self.rect.h)
        )
        inner_surf = pygame.Surface(inner_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            inner_surf,
            get_cfg("panel_bg_color"),
            (0, 0, inner_rect.w, inner_rect.h)
        )
        surface.blit(rect_surf, self.rect)
        surface.blit(inner_surf, inner_rect)

        spacing = fonts["text"].get_linesize()
        for i, surf in enumerate(self.__text_surfs):
            surface.blit(
                surf, 
                (inner_rect.x + get_cfg("panel_padding"),
                inner_rect.y + get_cfg("panel_padding") + i * spacing)
            )

    def delete(self):
        Panel.instances.remove(self)

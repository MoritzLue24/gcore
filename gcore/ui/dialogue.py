import time
import pygame
from .font import fonts
from ..config import get_cfg


class Dialogue:
    instances = []
    def __init__(
        self,
        text: str,
        options: list[str],
        letters_per_second: float,
        icon_path: str | None=None
    ):
        """the maximum number of options allowed is 3"""
        self.lines = text.split("\n")
        self.options = options
        self.letters_per_second = letters_per_second
        self.icon = pygame.image.load(icon_path) if icon_path != None else None
        
        self.__text_i = 0
        self.__line_i = 0 # if -1, the animation is finished
        self.__text_surfs = [
            fonts["dialogue"].render(line, False, (255, 255, 255))
            for line in self.lines
        ]
        self.__start_time = time.time()
        
        Dialogue.instances.append(self)

    @staticmethod
    def events(event: pygame.event.Event) -> int:
        """returns the selected option
        -1 means theres no opened dialogue / closed / skipped / text anim skip,
        0 means no option was selected,
        everything other represents the accordingly index of self.options"""

        if len(Dialogue.instances) == 0:
            return -1

        dialogue = Dialogue.instances[0]
        if event.type == pygame.KEYDOWN:
            opt_len = len(dialogue.options)

            if event.key == pygame.K_SPACE:
                if dialogue.__line_i != -1:
                    dialogue.__line_i = -1
                    return -1
                Dialogue.instances.pop(0)
                return -1
            elif event.key == pygame.K_1 and opt_len >= 1:
                return 1
            elif event.key == pygame.K_2 and opt_len >= 2:
                return 2
            elif event.key == pygame.K_3 and opt_len >= 3:
                return 3

        return 0

    @staticmethod
    def draw(surface: pygame.Surface):
        if len(Dialogue.instances) == 0:
            return

        dialogue: Dialogue = Dialogue.instances[0]

        current_time = time.time()
        if dialogue.__line_i != -1 and \
            current_time - dialogue.__start_time >= \
            1.0 / dialogue.letters_per_second:

            dialogue.__start_time = current_time
            if dialogue.__text_i >= len(dialogue.lines[dialogue.__line_i]):
                dialogue.__text_i = 0
                dialogue.__line_i += 1
                if dialogue.__line_i >= len(dialogue.lines):
                    dialogue.__line_i = -1
            else:
                dialogue.__text_i += 1

        outer_rect = pygame.Rect(
            (surface.get_size()[0] - get_cfg("dialogue_width")) // 2,
            (surface.get_size()[1] - get_cfg("dialogue_height")) // 1.1,
            get_cfg("dialogue_width"),
            get_cfg("dialogue_height")
        )
        inner_rect = pygame.Rect(
            outer_rect.x + get_cfg("dialogue_border_width"),
            outer_rect.y + get_cfg("dialogue_border_width"),
            outer_rect.width - 2 * get_cfg("dialogue_border_width"),
            outer_rect.height - 2 * get_cfg("dialogue_border_width")
        )
        pygame.draw.rect(surface, get_cfg("dialogue_border_color"), outer_rect)
        pygame.draw.rect(surface, get_cfg("dialogue_bg_color"), inner_rect)
        
        if dialogue.icon != None:
            surface.blit(
                dialogue.icon,
                (inner_rect.x + inner_rect.w -
                    dialogue.icon.get_size()[0] - get_cfg("dialogue_padding"),
                inner_rect.y + get_cfg("dialogue_padding"))
            )

        spacing = fonts["dialogue"].get_linesize()
        
        if dialogue.__line_i == -1:
            for i in range(len(dialogue.lines)):
                surface.blit(
                    dialogue.__text_surfs[i],
                    (inner_rect.x + get_cfg("dialogue_padding"),
                     inner_rect.y + get_cfg("dialogue_padding") + i * spacing)
                )
            return

        for i in range(dialogue.__line_i):
            surface.blit(
                dialogue.__text_surfs[i],
                (inner_rect.x + get_cfg("dialogue_padding"),
                 inner_rect.y + get_cfg("dialogue_padding") + i * spacing)
            )

        subtext = dialogue.lines[dialogue.__line_i][:dialogue.__text_i + 1]
        subtext_surf = fonts["dialogue"].render(subtext, False, (255, 255, 255))

        surface.blit(
            subtext_surf,
            (inner_rect.x + get_cfg("dialogue_padding"),
             inner_rect.y + get_cfg("dialogue_padding") +
                dialogue.__line_i * spacing)
        )
        

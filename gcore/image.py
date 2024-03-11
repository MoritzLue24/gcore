import pygame


def load_sheet(
    path: str,
    image_size: tuple[int, int]
) -> list[list[pygame.Surface]]:
    sheet = pygame.image.load(path).convert_alpha()
    images = []

    for i in range(sheet.get_height() // image_size[1]):
        row = []
        for j in range(sheet.get_width() // image_size[0]):
            row.append(sheet.subsurface(
                j * image_size[0],
                i * image_size[1],
                image_size[0],
                image_size[1])
            )
        images.append(row)
    return images

def is_empty(surface: pygame.Surface) -> bool:
    for y in range(surface.get_height()):
        for x in range(surface.get_width()):
            if surface.get_at((x, y)) != pygame.Color(0, 0, 0, 0):
                return False
    return True

import pygame


def load_sheet(
    path: str,
    image_size: tuple[int, int]
) -> list[list[pygame.Surface]]:
    sheet = pygame.image.load(path)
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

import pygame

from .image import load_sheet
from .config import get_cfg
from . import camera


class Tile:
    def __init__(self, name: str, color: pygame.Color, image: pygame.Surface):
        self.name = name
        self.color = color
        self.image = image
    
    def __copy__(self):
        return Tile(self.name, self.color, self.image)

def load_tileset(
    path: str,
    tile_size: tuple[int, int],
    config: dict[str, pygame.Color]
) -> list[Tile]:
    tiles = []
    i = 0
    for row in load_sheet(path, tile_size):
        for image in row:
            try:
                name, color = list(config.items())[i]
            except IndexError:
                raise ValueError("not enough config for each block")
            tiles.append(Tile(name, color, image))
            i += 1
    return tiles

class Tilemap:
    def __init__(self, tileset: list[Tile], path: str):
        self.__tiles = []
        for row in load_sheet(path, (1, 1)):
            tile_row = []
            for surface in row:
                tile = [
                    tile.__copy__() for tile in tileset
                    if tile.color == surface.get_at((0, 0))
                ]

                if len(tile) == 0:
                    raise ValueError("tile color does not exist in tileset")

                tile[0].image = pygame.transform.scale_by(tile[0].image, get_cfg("scale"))
                tile_row.append(tile[0])
            self.__tiles.append(tile_row)


    def get_at(self, pos: pygame.Vector2) -> Tile:
        """returns the tile on the rounded position
        (x, y corresponds the row, col of the tilemap)"""
        return self.__tiles[round(pos.y)][round(pos.x)]

    def draw(self, surface: pygame.Surface):
        for i, row in enumerate(self.__tiles):
            for j, tile in enumerate(row):
                surface.blit(
                    tile.image,
                    pygame.Vector2(j * tile.image.get_width(),
                        i * tile.image.get_height()) + camera.offset()
                )

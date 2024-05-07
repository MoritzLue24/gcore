import pygame

from .image import load_sheet
from .config import get_cfg
from . import camera


class Tile:
    def __init__(self, name: str, color: pygame.Color, collide: bool, image: pygame.Surface):
        self.name = name
        self.color = color
        self.collide = collide
        self.image = image
    
    def __copy__(self):
        return Tile(self.name, self.color, self.collide, self.image)

def load_tileset(
    path: str,
    config: dict[str, tuple[pygame.Color, bool]]
) -> list[Tile]:
    """the config has the following format:
    <tile-name>: [<tile-color>, <collide?>]"""
    tiles = []
    i = 0
    for row in load_sheet(path, get_cfg("tile_size")):
        for image in row:
            try:
                name, (color, collide) = list(config.items())[i]
            except IndexError:
                raise ValueError("not enough config for each block")
            tiles.append(Tile(name, color, collide, image))
            i += 1
    return tiles

class Tilemap:
    active = None
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
                
                tile[0].image = pygame.transform.scale_by(
                    tile[0].image,
                    get_cfg("scale")
                )
                tile_row.append(tile[0])
            self.__tiles.append(tile_row)
        Tilemap.active = self
    
    def enable(self):
        Tilemap.active = self

    def disable(self):
        Tilemap.active = None

    def get_at(self, pos: pygame.Vector2) -> Tile:
        """returns the tile on the rounded position
        (x, y corresponds the row, col of the tilemap)"""
        if Tilemap.active != self: raise ValueError("tilemap not active")
        return self.__tiles[round(pos.y)][round(pos.x)]
    
    def collision_point(
        self,
        entity_pos: pygame.Vector2,
        entity_dir: pygame.Vector2
    ) -> pygame.Vector2:
        """if the entity will be colliding with a tile with the
        'collide' attribute, get the point of collision so it can be set as
        the new entites collision.
        this function returns pos + dir if theres no collision."""
        if entity_dir.magnitude() == 0: return entity_pos
        
        tile_cols = []
        for r, row in enumerate(self.__tiles):
            for c, tile in enumerate(row):
                if not tile.collide: continue

                rect = pygame.Rect(r, c, 1, 1)
                border_cols = []
                sides = [
                    (pygame.Vector2(rect.x, rect.y), pygame.Vector2(rect.w, 0)),
                    (pygame.Vector2(rect.x, rect.y), pygame.Vector2(0, rect.h)),
                    (pygame.Vector2(rect.x + rect.w, rect.y), pygame.Vector2(0, rect.h)),
                    (pygame.Vector2(rect.x, rect.y + rect.h), pygame.Vector2(rect.w, 0))
                ]

                for side in sides:
                    x1, y1 = entity_pos
                    x2, y2 = entity_pos + entity_dir
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

                    # check if intersection point lies within the range of both lines
                    if min(x1, x2) <= intersection_x <= max(x1, x2) and \
                        min(y1, y2) <= intersection_y <= max(y1, y2) and \
                        min(x3, x4) <= intersection_x <= max(x3, x4) and \
                        min(y3, y4) <= intersection_y <= max(y3, y4):
                        border_cols.append(pygame.Vector2(intersection_x, intersection_y))

                border_cols.sort(key=lambda x: (entity_pos - x).magnitude())
                if border_cols:
                    tile_cols.append(border_cols[0])

        tile_cols.sort(key=lambda x: (entity_pos - x).magnitude())
        if not tile_cols:
            return entity_pos + entity_dir
        return tile_cols[0]

    def draw(self, surface: pygame.Surface):
        if Tilemap.active != self: return
        for i, row in enumerate(self.__tiles):
            for j, tile in enumerate(row):
                surface.blit(
                    tile.image,
                    pygame.Vector2(j * tile.image.get_width(),
                        i * tile.image.get_height()) + camera.offset()
                )

import pygame


class LinesAreParallel(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

def line_intersection(
    a: pygame.Vector2,
    dir_a: pygame.Vector2,
    b: pygame.Vector2,
    dir_b: pygame.Vector2
) -> tuple[pygame.Vector2, bool]:
    """returns the point of intersection,
    and true if the point lies withing the ranges of dir a, b.
    if the lines are parallel, returns (a, True)"""
    x1, y1 = a
    x2, y2 = a + dir_a
    x3, y3 = b
    x4, y4 = b + dir_b

    slope1 = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    slope2 = (y4 - y3) / (x4 - x3) if x4 - x3 != 0 else float('inf')
    if slope1 == slope2: raise LinesAreParallel()

    intersection = pygame.Vector2(
        ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) *
            (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) *
            (x3 - x4)),
        ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) *
            (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) *
            (x3 - x4))
    )

    # check if intersection point lies within the range of both lines
    col_x1 = min(x1, x2) <= intersection.x <= max(x1, x2)
    col_y1 = min(y1, y2) <= intersection.y <= max(y1, y2)
    col_x2 = min(x3, x4) <= intersection.x <= max(x3, x4)
    col_y2 = min(y3, y4) <= intersection.y <= max(y3, y4)

    return (intersection, col_x1 and col_y1 and col_x2 and col_y2)
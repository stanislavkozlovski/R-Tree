"""
Module that contains functions for creating new Point objects
"""
from point import Point


# TODO: Move to Point class
def move_left_of(point_a: Point, point_b: Point) -> Point:
    """
    Creates a new Point object, the same as point_a, moved MOVE_DISTANCE left of point_b
    """
    return Point(x=point_b.x - Point.MOVE_DISTANCE, y=point_a.y)


def move_right_of(point_a: Point, point_b: Point) -> Point:
    """
    Creates a new Point object, the same as point_a, moved MOVE_DISTANCE right of point_b
    """
    return Point(x=point_b.x + Point.MOVE_DISTANCE, y=point_a.y)


def move_above(point_a: Point, point_b: Point) -> Point:
    """
    Creates a new Point object, the same as point_a, moved MOVE_DISTANCE above point_b
    """
    return Point(x=point_a.x, y=point_b.y + Point.MOVE_DISTANCE)


def move_below(point_a: Point, point_b: Point) -> Point:
    """
    Creates a new Point object, the same as point_a, moved MOVE_DISTANCE below point_b
    """
    return Point(x=point_a.x, y=point_b.y - Point.MOVE_DISTANCE)

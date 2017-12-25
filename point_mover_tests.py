from unittest import TestCase

from point import Point
from point_mover import move_right_of, move_left_of, move_below, move_above


class PointMoverTests(TestCase):
    def setUp(self):
        self.point_a = Point(10, 10)

    def test_move_above_moves_by_MOVE_DISTANCE(self):
        point_b = Point(10, 12)

        new_point: Point = move_above(self.point_a, point_b)
        self.assertEqual(self.point_a.x, 10)
        self.assertEqual(self.point_a.y, 10)
        self.assertEqual(new_point.x, point_b.x)
        self.assertEqual(new_point.y, point_b.y + Point.MOVE_DISTANCE)

    def test_move_below_moves_by_MOVE_DISTANCE(self):
        point_b = Point(10, 5)
        new_point = move_below(self.point_a, point_b)

        self.assertEqual(self.point_a.x, 10)
        self.assertEqual(self.point_a.y, 10)
        self.assertEqual(new_point.x, self.point_a.x)
        self.assertEqual(new_point.y, point_b.y - Point.MOVE_DISTANCE)

    def test_move_left_of_moves_by_MOVE_DISTANCE(self):
        point_b = Point(5, 10)

        new_point = move_left_of(self.point_a, point_b)
        self.assertEqual(self.point_a.x, 10)
        self.assertEqual(self.point_a.y, 10)
        self.assertEqual(new_point.y, self.point_a.y)
        self.assertEqual(new_point.x, point_b.x - Point.MOVE_DISTANCE)

    def test_move_right_of_moves_by_MOVE_DISTANCE(self):
        point_b = Point(12, 10)

        new_point = move_right_of(self.point_a, point_b)

        self.assertEqual(self.point_a.x, 10)
        self.assertEqual(self.point_a.y, 10)
        self.assertEqual(new_point.y, self.point_a.y)
        self.assertEqual(new_point.x, point_b.x + Point.MOVE_DISTANCE)

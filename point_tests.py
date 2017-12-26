from unittest import TestCase
from point import Point


class PointTests(TestCase):
    def setUp(self):
        self.point_a = Point(10, 10)

    def test_height_from_returns_absolute_difference(self):
        height = self.point_a.height_from(Point(x=10, y=12))
        self.assertEqual(height, 2)

    def test_width_from_returns_absolute_difference(self):
        width = self.point_a.width_from(Point(x=12, y=10))
        self.assertEqual(width, 2)

    def test_move_above_raises_error_if_point_is_above_already(self):
        point_b = Point(10, 5)
        with self.assertRaises(Point.InvalidMoveError):
            self.point_a.move_above(point_b)

    def test_move_above_doesnt_raise_error_if_point_is_above_less_than_MOVE_DISTANCE(self):
        point_b = Point(10, self.point_a.y - (Point.MOVE_DISTANCE - 0.1))
        self.point_a.move_above(point_b)

    def test_move_above_moves_by_MOVE_DISTANCE(self):
        point_b = Point(10, 12)
        expected_y = point_b.y + Point.MOVE_DISTANCE

        self.point_a.move_above(point_b)
        self.assertEqual(self.point_a.y, expected_y)

    def test_move_below_raises_error_if_point_is_below_already(self):
        point_b = Point(10, 12)
        with self.assertRaises(Point.InvalidMoveError):
            self.point_a.move_below(point_b)

    def test_move_below_doesnt_raise_error_if_point_is_below_less_than_MOVE_DISTANCE(self):
        point_b = Point(10, self.point_a.y + (Point.MOVE_DISTANCE - 0.1))
        self.point_a.move_below(point_b)

    def test_move_below_moves_by_MOVE_DISTANCE(self):
        point_b = Point(10, 5)
        expected_y = point_b.y - Point.MOVE_DISTANCE

        self.point_a.move_below(point_b)
        self.assertEqual(self.point_a.y, expected_y)

    def test_move_left_of_raises_error_if_point_is_left_of_already(self):
        point_b = Point(15, 10)
        with self.assertRaises(Point.InvalidMoveError):
            self.point_a.move_left_of(point_b)

    def test_move_left_of_doesnt_raise_error_if_point_is_left_of_less_than_MOVE_DISTANCE(self):
        point_b = Point(self.point_a.x + (Point.MOVE_DISTANCE - 0.1), 10)
        self.point_a.move_left_of(point_b)

    def test_move_left_of_moves_by_MOVE_DISTANCE(self):
        point_b = Point(5, 10)
        expected_x = point_b.x - Point.MOVE_DISTANCE

        self.point_a.move_left_of(point_b)
        self.assertEqual(self.point_a.x, expected_x)

    def test_move_right_of_raises_error_if_point_is_right_of_already(self):
        point_b = Point(5, 10)
        with self.assertRaises(Point.InvalidMoveError):
            self.point_a.move_right_of(point_b)

    def test_move_right_of_doesnt_raise_error_if_point_is_right_of_less_than_MOVE_DISTANCE(self):
        point_b = Point(self.point_a.x - (Point.MOVE_DISTANCE - 0.1), 10)
        self.point_a.move_right_of(point_b)

    def test_move_right_of_moves_by_MOVE_DISTANCE(self):
        point_b = Point(12, 10)
        expected_x = point_b.x + Point.MOVE_DISTANCE

        self.point_a.move_right_of(point_b)
        self.assertEqual(self.point_a.x, expected_x)

    def test_equals_returns_true_when_equal_coordinates(self):
        self.assertEqual(Point(12, 10), Point(12, 10))

    def test_equals_returns_false_when_different_coordinates(self):
        self.assertNotEqual(Point(15, 10), Point(12, 10))

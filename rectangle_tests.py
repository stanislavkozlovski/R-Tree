import unittest
from copy import deepcopy

from rectangle import Point, Rectangle, RectangleResizer


class RectangleTests(unittest.TestCase):
    def setUp(self):
        self.rect_a = Rectangle(top_left=Point(2, 4), bottom_right=Point(4, 3))

    def test_raises_error_if_invalid_points_given(self):
        with self.assertRaises(Rectangle.InvalidRectangleError):
            # Bottom Right point cannot be above Top Left
            Rectangle(top_left=Point(1, 1), bottom_right=Point(2, 2))
        with self.assertRaises(Rectangle.InvalidRectangleError):
            # Bottom Right point cannot be left of Top Left
            Rectangle(top_left=Point(1, 1), bottom_right=Point(0, 0))

    def test_equals_return_true_when_points_are_same(self):
        rect_b = Rectangle(top_left=Point(2, 4), bottom_right=Point(4, 3))
        self.assertEqual(self.rect_a, rect_b)

    def test_equals_return_false_when_points_are_not_the_same(self):
        rect_b = Rectangle(top_left=Point(2, 4), bottom_right=Point(4, 1))
        self.assertNotEqual(self.rect_a, rect_b)

    def test_width_height_and_area_are_set(self):
        rect = Rectangle(top_left=Point(2, 4), bottom_right=Point(4, 2))
        self.assertEqual(rect.width, 2)
        self.assertEqual(rect.height, 2)
        self.assertEqual(rect.area, 4)

    def test_calculate_area(self):
        expected_height = 10
        expected_width = 30
        expected_area = expected_height * expected_width

        height, width, area = Rectangle.calculate_area(Point(10, 10), Point(40, 20))

        self.assertEqual(expected_height, height)
        self.assertEqual(expected_width, width)
        self.assertEqual(expected_area, area)

    def test_calculate_bottom_left_point(self):
        expected_point = Point(2, 3)
        self.assertEqual(expected_point, self.rect_a.calculate_bottom_left())

    def test_calculate_top_right_point(self):
        expected_point = Point(4, 4)
        self.assertEqual(expected_point, self.rect_a.calculate_top_right())

    def test_intersects_returns_false_when_rect_above(self):
        """
       ---------
       |   B   |
       ---------
        ---------
       |         |
       |   A     |
        _________
        """
        self.rect_b = Rectangle(top_left=Point(2, 5), bottom_right=Point(3, 4.5))

        self.assertFalse(self.rect_a.is_intersecting(self.rect_b))
        self.assertFalse(self.rect_b.is_intersecting(self.rect_a))

    def test_intersects_returns_false_when_rect_below(self):
        """
        ---------
       |         |
       |   A     |
        _________

        ----------------
       |                |
       |      B         |
       |                |
       ------------------
        """
        self.rect_b = Rectangle(top_left=Point(2, 2), bottom_right=Point(5, 1))

        self.assertFalse(self.rect_a.is_intersecting(self.rect_b))
        self.assertFalse(self.rect_b.is_intersecting(self.rect_a))

    def test_intersects_returns_true_when_intersect(self):
        """
        ---------
       |         |
       |   A-----|------
        ____|____      |
            |    B     |
            ___________

        """
        self.rect_b = Rectangle(top_left=Point(3, 3.5), bottom_right=Point(5, 2))

        self.assertTrue(self.rect_a.is_intersecting(self.rect_b))
        self.assertTrue(self.rect_b.is_intersecting(self.rect_a))

    def test_is_bounding_returns_true_when_bounds(self):
        self.rect_b = Rectangle(top_left=Point(2.5, 3.5), bottom_right=Point(3.5, 3.25))

        self.assertTrue(self.rect_a.is_bounding(self.rect_b))
        self.assertFalse(self.rect_b.is_bounding(self.rect_a))

    def test_is_bounding_returns_false_when_exact_same(self):
        self.rect_b = Rectangle(top_left=Point(2, 4), bottom_right=Point(4, 3))

        self.assertFalse(self.rect_b.is_bounding(self.rect_a))
        self.assertFalse(self.rect_a.is_bounding(self.rect_b))

    def test_is_bounding_by_returns_false_when_overlapping(self):
        self.rect_b = Rectangle(top_left=Point(3.5, 3.5), bottom_right=Point(4.5, 2.5))

        self.assertFalse(self.rect_b.is_bounding(self.rect_a))
        self.assertFalse(self.rect_a.is_bounding(self.rect_b))

    def test_is_bounding_by_returns_false_when_far_off(self):
        self.rect_b = Rectangle(top_left=Point(6, 2), bottom_right=Point(8, 1))

        self.assertFalse(self.rect_b.is_bounding(self.rect_a))
        self.assertFalse(self.rect_a.is_bounding(self.rect_b))

    def test_is_bounded_by_returns_true_when_bounded(self):
        self.rect_b = Rectangle(top_left=Point(2.5, 3.5), bottom_right=Point(3.5, 3.25))

        self.assertTrue(self.rect_b.is_bounded_by(self.rect_a))
        self.assertFalse(self.rect_a.is_bounded_by(self.rect_b))

    def test_is_bounded_by_returns_false_when_exact_same(self):
        self.rect_b = Rectangle(top_left=Point(2, 4), bottom_right=Point(4, 3))

        self.assertFalse(self.rect_b.is_bounded_by(self.rect_a))
        self.assertFalse(self.rect_a.is_bounded_by(self.rect_b))

    def test_is_bounded_by_returns_false_when_overlapping(self):
        self.rect_b = Rectangle(top_left=Point(3.5, 3.5), bottom_right=Point(4.5, 2.5))

        self.assertFalse(self.rect_b.is_bounded_by(self.rect_a))
        self.assertFalse(self.rect_a.is_bounded_by(self.rect_b))

    def test_is_bounded_by_returns_false_when_far_off(self):
        self.rect_b = Rectangle(top_left=Point(6, 2), bottom_right=Point(8, 1))

        self.assertFalse(self.rect_b.is_bounded_by(self.rect_a))
        self.assertFalse(self.rect_a.is_bounded_by(self.rect_b))

    def test_distance_between_intersecting_is_zero(self):
        other_rect = Rectangle(top_left=Point(3, 3.5), bottom_right=Point(5, 2))
        self.assertEqual(0, self.rect_a.distance_between(other_rect))

    def test_distance_between_rectangle_that_is_strictly_above(self):
        """
     -------------
     |   B        |
     ------------
        ---------
        |         |
        |   A     |
        _________
        """
        other_rect = Rectangle(Point(1, 6), Point(4, 5))
        expected_distance = self.rect_a.calculate_top_right().distance_to(other_rect.bottom_right)
        self.assertEqual(expected_distance, self.rect_a.distance_between(other_rect))

    def test_distance_between_rectangle_that_is_strictly_below(self):
        """
        ---------
       |         |
       |   A     |
        _________
        -------------
        |   B        |
        ------------
        """
        other_rect = Rectangle(Point(2, 2), Point(5, 1))
        expected_distance = self.rect_a.calculate_bottom_left().distance_to(other_rect.top_left)
        self.assertEqual(expected_distance, self.rect_a.distance_between(other_rect))

    def test_distance_between_rectangle_that_is_strictly_left(self):
        """
       --------      ---------
       |       |    |         |
       |       |    |   A     |
       |  B    |     _________
       |       |
       ____ ____
        """
        other_rect = Rectangle(top_left=Point(0.5, 4), bottom_right=Point(1.5, 3))
        expected_distance = self.rect_a.top_left.distance_to(other_rect.calculate_top_right())
        self.assertEqual(expected_distance, self.rect_a.distance_between(other_rect))

    def test_distance_between_rectangle_that_is_strictly_right(self):
        """
            ---------      ---------
           |         |    |         |
           |   A     |    |    B    |
            _________     |         |
                          |         |
                           ----------
        """
        other_rect = Rectangle(top_left=Point(6, 4), bottom_right=Point(10, 1))
        expected_distance = self.rect_a.calculate_top_right().distance_to(other_rect.top_left)
        self.assertEqual(expected_distance, self.rect_a.distance_between(other_rect))

    def test_distance_between_rectangle_that_is_right_and_above(self):
        """
                            ---------
                           |         |
                           |    B    |
                           |         |
                           |         |
                            ----------

            ---------
           |         |
           |   A     |
            _________
        """
        other_rect = Rectangle(top_left=Point(6, 6), bottom_right=Point(8, 5))
        expected_distance = self.rect_a.calculate_top_right().distance_to(other_rect.calculate_bottom_left())
        self.assertEqual(expected_distance, self.rect_a.distance_between(other_rect))

    def test_distance_between_rectangle_that_is_left_and_above(self):
        """
       ---------
      |         |
      |    B    |
      |         |
      |         |
       ----------

                   ---------
                  |         |
                  |   A     |
                   _________
        """
        other_rect = Rectangle(top_left=Point(0.5, 6), bottom_right=Point(1.5, 5))
        expected_distance = self.rect_a.top_left.distance_to(other_rect.bottom_right)
        self.assertEqual(expected_distance, self.rect_a.distance_between(other_rect))

    def test_distance_between_rectangle_that_is_right_and_below(self):
        """
            ---------
           |         |
           |   A     |
            _________

                         ---------
                        |         |
                        |    B    |
                        |         |
                        |         |
                         ----------
        """
        other_rect = Rectangle(top_left=Point(5, 2), bottom_right=Point(7, 1))
        expected_distance = self.rect_a.bottom_right.distance_to(other_rect.top_left)
        self.assertEqual(expected_distance, self.rect_a.distance_between(other_rect))

    def test_distance_between_rectangle_that_is_left_and_below(self):
        """
                   ---------
                  |         |
                  |   A     |
                   _________

     ---------
    |         |
    |    B    |
    |         |
    |         |
     ----------
        """
        other_rect = Rectangle(top_left=Point(1, 2), bottom_right=Point(1.5, 1))
        expected_distance = self.rect_a.calculate_bottom_left().distance_to(other_rect.calculate_top_right())
        self.assertEqual(expected_distance, self.rect_a.distance_between(other_rect))

    def test_containing(self):
        """
        The class method containing() should return a
            Rectangle object that can contain the passed rectangle
        """
        expected_tl = Point(self.rect_a.top_left.x - Point.MOVE_DISTANCE, self.rect_a.top_left.y + Point.MOVE_DISTANCE)
        expected_br = Point(self.rect_a.bottom_right.x + Point.MOVE_DISTANCE, self.rect_a.bottom_right.y - Point.MOVE_DISTANCE)
        expected_rectangle = Rectangle(top_left=expected_tl, bottom_right=expected_br)

        self.assertEqual(expected_rectangle, Rectangle.containing(self.rect_a))


class RectangleResizingTests(unittest.TestCase):
    def setUp(self):
        self.rect_dummy = Rectangle(Point(10, 10), Point(20, 5))

    def test_expand_to_expands_rectangle(self):
        rectangle = Rectangle(Point(11, 9), Point(15, 7))
        rectangle.expand_to(self.rect_dummy)
        self.assertTrue(rectangle.is_bounding(self.rect_dummy))

    def test_expand_to_updates_area_width_height(self):
        rectangle = Rectangle(Point(11, 9), Point(15, 7))
        orig_w, orig_h, orig_a = rectangle.width, rectangle.height, rectangle.area

        rectangle.expand_to(self.rect_dummy)

        self.assertNotEqual(orig_a, rectangle.area)
        self.assertNotEqual(orig_h, rectangle.height)
        self.assertNotEqual(orig_w, rectangle.width)

    def test_expanded_to_expands_rectangle_and_retains_bottom_right_point_if_it_already_covers(self):
        expected_br = Point(21, 4)
        rectangle = Rectangle(top_left=Point(11, 9), bottom_right=Point(21, 4))

        rectangle.expand_to(self.rect_dummy)

        self.assertTrue(rectangle.is_bounding(self.rect_dummy))
        self.assertEqual(expected_br, rectangle.bottom_right)

    def test_expanded_to_expands_rectangle_and_retains_top_left_point_if_it_already_covers(self):
        expected_tl = Point(9, 11)
        rectangle = Rectangle(top_left=Point(9, 11), bottom_right=Point(19, 9))

        rectangle.expand_to(self.rect_dummy)

        self.assertTrue(rectangle.is_bounding(self.rect_dummy))
        self.assertEqual(expected_tl, rectangle.top_left)

    def test_expanded_to_expands_only_x_axis_if_applicable(self):
        """
        We want it to keep as much of the original coordinates as possible
        """
        rectangle = Rectangle(top_left=Point(6, 11), bottom_right=Point(7, 4))

        rectangle.expand_to(self.rect_dummy)

        self.assertEqual(rectangle.top_left.y, 11)
        self.assertEqual(rectangle.bottom_right.y, 4)

    def test_expanded_to_expands_only_y_axis_if_applicable(self):
        """
        We want it to keep as much of the original coordinates as possible
        """
        rectangle = Rectangle(top_left=Point(9, 11), bottom_right=Point(21, 6))

        rectangle.expand_to(self.rect_dummy)

        self.assertEqual(rectangle.top_left.x, 9)
        self.assertEqual(rectangle.bottom_right.x, 21)

    def test_expanded_to_raises_error_if_rectangle_already_contains_other_rect(self):
        rectangle = Rectangle(top_left=Point(9, 11), bottom_right=Point(21, 4))
        with self.assertRaises(RectangleResizer.ResizeError):
            rectangle.expand_to(self.rect_dummy)


class RectangleResizerTests(unittest.TestCase):
    def setUp(self):
        self.rectangle = Rectangle(Point(10, 10), Point(20, 5))

    def test_expanded_to_expands_rectangle(self):
        other_rect = Rectangle(Point(11, 9), Point(15, 7))
        new_rect = RectangleResizer.rectangle_expanded_to(other_rect, self.rectangle)
        self.assertTrue(new_rect.is_bounding(self.rectangle))

    def test_expanded_to_doesnt_modify_original_rectangles(self):
        other_rect = Rectangle(Point(11, 9), Point(15, 7))
        orig_rect = deepcopy(self.rectangle)
        orig_other_rect = deepcopy(other_rect)

        new_rect = RectangleResizer.rectangle_expanded_to(other_rect, self.rectangle)

        self.assertEqual(orig_rect, self.rectangle)
        self.assertEqual(orig_other_rect, other_rect)

    def test_expanded_to_expands_rectangle_and_retains_bottom_right_point_if_it_already_covers(self):
        expected_br = Point(21, 4)
        other_rect = Rectangle(top_left=Point(11, 9), bottom_right=Point(21, 4))

        new_rect = RectangleResizer.rectangle_expanded_to(other_rect, self.rectangle)

        self.assertTrue(new_rect.is_bounding(self.rectangle))
        self.assertEqual(expected_br, new_rect.bottom_right)

    def test_expanded_to_expands_rectangle_and_retains_top_left_point_if_it_already_covers(self):
        expected_tl = Point(9, 11)
        other_rect = Rectangle(top_left=Point(9, 11), bottom_right=Point(19, 9))

        new_rect = RectangleResizer.rectangle_expanded_to(other_rect, self.rectangle)

        self.assertTrue(new_rect.is_bounding(self.rectangle))
        self.assertEqual(expected_tl, new_rect.top_left)

    def test_expanded_to_expands_only_x_axis_if_applicable(self):
        """
        We want it to keep as much of the original coordinates as possible
        """
        other_rect = Rectangle(top_left=Point(6, 11), bottom_right=Point(7, 4))
        new_rect = RectangleResizer.rectangle_expanded_to(other_rect, self.rectangle)

        self.assertEqual(new_rect.top_left.y, 11)
        self.assertEqual(new_rect.bottom_right.y, 4)

    def test_expanded_to_expands_only_y_axis_if_applicable(self):
        """
        We want it to keep as much of the original coordinates as possible
        """
        other_rect = Rectangle(top_left=Point(9, 11), bottom_right=Point(21, 6))
        new_rect = RectangleResizer.rectangle_expanded_to(other_rect, self.rectangle)

        self.assertEqual(new_rect.top_left.x, 9)
        self.assertEqual(new_rect.bottom_right.x, 21)

    def test_expanded_to_raises_error_if_rectangle_already_contains_other_rect(self):
        other_rect = Rectangle(top_left=Point(9, 11), bottom_right=Point(21, 4))
        with self.assertRaises(RectangleResizer.ResizeError):
            RectangleResizer.rectangle_expanded_to(other_rect, self.rectangle)


if __name__ == '__main__':
    unittest.main()

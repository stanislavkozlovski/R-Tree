import unittest

from rectangle import Point, Rectangle


class RectangleTests(unittest.TestCase):
    def setUp(self):
        self.rect_a = Rectangle(top_left=Point(2, 4), bottom_right=Point(4, 3))

    def test_width_height_and_area_are_set(self):
        rect = Rectangle(top_left=Point(2, 4), bottom_right=Point(4, 6))
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
        self.rect_a = Rectangle(top_left=Point(2, 4), bottom_right=Point(4, 3))
        other_rect = Rectangle(top_left=Point(1, 2), bottom_right=Point(1.5, 1))
        expected_distance = self.rect_a.calculate_bottom_left().distance_to(other_rect.calculate_top_right())
        self.assertEqual(expected_distance, self.rect_a.distance_between(other_rect))

if __name__ == '__main__':
    unittest.main()

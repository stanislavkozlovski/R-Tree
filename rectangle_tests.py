from unittest import TestCase
from rectangle import Point, Rectangle


class RectangleTests(TestCase):
    def setUp(self):
        self.rect_a = Rectangle(top_left=Point(2,4), bottom_right=Point(4, 3))

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

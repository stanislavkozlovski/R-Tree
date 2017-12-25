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

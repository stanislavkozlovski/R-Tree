class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_left_of(self, other_point: 'Point'):
        return self.x < other_point.x

    def is_right_of(self, other_point: 'Point'):
        return self.x > other_point.x

    def is_above(self, other_point: 'Point'):
        return self.y > other_point.y

    def is_below(self, other_point: 'Point'):
        return self.y < other_point.y


class Rectangle:
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def is_intersecting(self, other_rect: 'Rectangle'):
        """
        :return: Boolean, indicating if both rectangles intersect/overlap
        """
        if (self.top_left.is_right_of(other_rect.bottom_right)
                or self.bottom_right.is_left_of(other_rect.top_left)):
            return False

        if (self.top_left.is_below(other_rect.bottom_right)
                or self.bottom_right.is_above(other_rect.top_left)):
            return False

        return True

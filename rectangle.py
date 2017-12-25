from point import Point


class Rectangle:
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.height = top_left.height_from(bottom_right)
        self.width = top_left.width_from(bottom_right)
        self.area = self.height * self.width

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

    def is_bounding(self, other_rect: 'Rectangle'):
        """
        :return: Boolean, indicating if this rectangle contains the other inside itself
            NOTE: if Rectangle A == Rectangle B, A does not contain B and B does not contain A
        """
        return (self.top_left.is_above(other_rect.top_left)
                and self.top_left.is_left_of(other_rect.top_left)
                and self.bottom_right.is_below(other_rect.bottom_right)
                and self.bottom_right.is_right_of(other_rect.bottom_right))

    def is_bounded_by(self, other_rect: 'Rectangle'):
        """
        :return: Boolean, indicating if this rectangle is contained inside the other rectangle
            NOTE: if Rectangle A == Rectangle B, A does not contain B and B does not contain A
        """

        return other_rect.is_bounding(self)

from point import Point

class Rectangle:
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.height, self.width, self.area = self.calculate_area(top_left, bottom_right)

    def calculate_bottom_left(self) -> Point:
        """
        :return: This rectangle's Bottom Left Point
            Note: This state is not kept in the class
        """
        return Point(x=self.top_left.x, y=self.bottom_right.y)

    def calculate_top_right(self) -> Point:
        """
        :return: This rectangle's Top Right Point
            Note: This state is not kept in the class
        """
        return Point(x=self.bottom_right.x, y=self.top_left.y)

    @staticmethod
    def calculate_area(top_left_point: Point, bottom_right_point: Point) -> (int, int, int):
        """
        Calculates the height, width and area of a Rectangle,
            given its top left and bottom right points
        """
        height = top_left_point.height_from(bottom_right_point)
        width = top_left_point.width_from(bottom_right_point)
        area = height * width

        return height, width, area

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

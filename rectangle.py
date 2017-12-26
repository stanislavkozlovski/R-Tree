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

    @classmethod
    def containing(cls, other_rect: 'Rectangle'):
        """
        Returns a new Rectangle object which can contain the given rectangle with MOVE_DISTANCE to spare
        e.g Rectangle.containing(Rect(10, 10, 20, 20)) => Rect(11, 11, 21, 21)
        """
        from point_mover import move_left_of, move_above, move_right_of, move_below

        top_left = move_above(move_left_of(Point(0, 0), other_rect.top_left), other_rect.top_left)
        bottom_right = move_below(move_right_of(Point(0, 0), other_rect.bottom_right), other_rect.bottom_right)

        return cls(top_left=top_left, bottom_right=bottom_right)

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

    def distance_between(self, other_rect: 'Rectangle') -> float:
        """
        Returns the minimum distance between two rectangle's closest points
        """
        is_left = self.bottom_right.is_left_of(other_rect.top_left)
        is_above = self.bottom_right.is_above(other_rect.top_left)
        is_below = self.top_left.is_below(other_rect.bottom_right)
        is_right = self.top_left.is_right_of(other_rect.bottom_right)

        if self.is_intersecting(other_rect):
            return 0
        if is_left and is_above:
            closest_points = [self.bottom_right, other_rect.top_left]
        elif is_left and is_below:
            closest_points = [self.calculate_top_right(), other_rect.calculate_bottom_left()]
        elif is_right and is_above:
            closest_points = [self.calculate_bottom_left(), other_rect.calculate_top_right()]
        elif is_right and is_below:
            closest_points = [self.top_left, other_rect.bottom_right]
        elif is_right:
            closest_points = [self.calculate_bottom_left(), other_rect.bottom_right, self.top_left, other_rect.calculate_top_right()]
        elif is_left:
            closest_points = [self.bottom_right, other_rect.calculate_bottom_left(), self.calculate_top_right(), other_rect.top_left]
        elif is_above:
            closest_points = [self.calculate_bottom_left(), other_rect.top_left, self.bottom_right, other_rect.calculate_top_right()]
        elif is_below:
            closest_points = [self.top_left, other_rect.calculate_bottom_left(), self.calculate_top_right(), other_rect.bottom_right]
        else:
            raise NotImplementedError()

        pairs = [(i, closest_points[idx+1]) for idx, i in enumerate(closest_points) if idx % 2 == 0]
        return min(point_a.distance_to(point_b) for (point_a, point_b) in pairs)

    def __eq__(self, other: 'Rectangle'):
        return self.bottom_right == other.bottom_right and self.top_left == other.top_left

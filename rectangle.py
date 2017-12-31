from copy import deepcopy

from point import Point


class Rectangle:
    class InvalidRectangleError(Exception):
        pass

    def __init__(self, top_left: Point, bottom_right: Point):
        self._check_contraints(top_left, bottom_right)
        self.resizer = RectangleResizer(self)
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.height, self.width, self.area = self.calculate_area(top_left, bottom_right)

    @classmethod
    def _check_contraints(cls, top_left: Point, bottom_right: Point):
        if not top_left.is_left_of(bottom_right) or not top_left.is_above(bottom_right):
            raise cls.InvalidRectangleError("Rectangle is not valid!")

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

    def recalculate_area(self):
        """
        Recalculates this Rectangle's area, height and width
        """
        self.height, self.width, self.area = self.calculate_area(self.top_left, self.bottom_right)

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

    def expand_to(self, other_rectangle: 'Rectangle'):
        """
        Expands the Rectangle to accommodate the given rectangle.
        Raises an error if it already accommodates it
        """
        self.resizer.expand_to(other_rectangle)
        self.recalculate_area()

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

    def __hash__(self):
        return hash(f'{hash(self.bottom_right)}{hash(self.top_left)}')


class RectangleResizer:
    """
    Adjustment-type class which deals with resizing rectangles
    """
    class ResizeError(Exception):
        pass

    def __init__(self, rectangle: Rectangle):
        self.rectangle = rectangle

    def expand_to(self, other_rect: Rectangle):
        """
        Expands the Rectangle to accommodate the given rectangle.
        Raises an error if it already accommodates it
        """
        if self.rectangle.is_bounding(other_rect):
            raise self.ResizeError('Rectangle is big enough to contain rectangle_b')
        self._expand_rectangle_points(self.rectangle.top_left, self.rectangle.bottom_right, other_rect)

    @classmethod
    def rectangle_expanded_to(cls, rectangle_a: Rectangle, rectangle_b: Rectangle) -> Rectangle:
        """
        Returns a new Rectangle object, derived from expanding rectangle_a to accommodate rectangle_b
        """
        if rectangle_a.is_bounding(rectangle_b):
            raise cls.ResizeError('Rectangle is big enough to contain rectangle_b')

        top_left: Point = deepcopy(rectangle_a.top_left)
        bottom_right: Point = deepcopy(rectangle_a.bottom_right)

        cls._expand_rectangle_points(top_left, bottom_right, rectangle_b)

        return Rectangle(top_left, bottom_right)

    @staticmethod
    def _expand_rectangle_points(top_left: Point, bottom_right: Point, rectangle_b: Rectangle):
        """
        Given two points, expands them to contain rectangle_b
        """
        if not top_left.is_left_of(rectangle_b.top_left):
            top_left.move_left_of(rectangle_b.top_left)
        if not top_left.is_above(rectangle_b.top_left):
            top_left.move_above(rectangle_b.top_left)
        if not bottom_right.is_below(rectangle_b.bottom_right):
            bottom_right.move_below(rectangle_b.bottom_right)
        if not bottom_right.is_right_of(rectangle_b.bottom_right):
            bottom_right.move_right_of(rectangle_b.bottom_right)

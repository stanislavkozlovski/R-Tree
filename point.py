class Point:
    class InvalidMoveError(Exception):
        pass

    # The distance at which the move_xxx methods will check
    MOVE_DISTANCE = 1

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

    def move_below(self, other_point: 'Point'):
        """
        Changes this Point's Y axis to be below other_points'
        """
        if self.is_below(other_point) and other_point.y - self.y >= self.MOVE_DISTANCE:
            raise self.InvalidMoveError("Point is already below other point!")

        self.y = other_point.y - self.MOVE_DISTANCE

    def move_above(self, other_point: 'Point'):
        """
        Changes this Point's Y axis to be above other_points'
        """
        if self.is_above(other_point) and self.y - other_point.y >= self.MOVE_DISTANCE:
            raise self.InvalidMoveError("Point is already above other point!")

        self.y = other_point.y + self.MOVE_DISTANCE

    def move_right_of(self, other_point: 'Point'):
        """
        Changes this Point's X axis to be right of other_points'
        """
        if self.is_right_of(other_point) and self.x - other_point.x >= self.MOVE_DISTANCE:
            raise self.InvalidMoveError("Point is already right of point!")

        self.x = other_point.x + self.MOVE_DISTANCE

    def move_left_of(self, other_point: 'Point'):
        """
        Changes this Point's X axis to be left of other_points'
        """
        if self.is_left_of(other_point) and other_point.x - self.x >= self.MOVE_DISTANCE:
            raise self.InvalidMoveError("Point is already left of point!")

        self.x = other_point.x - self.MOVE_DISTANCE

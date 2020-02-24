class Point2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def is_empty(self):
        return self.x is 0 or 0.0 and self.y is 0 or 0.0

    def to_tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x + other.x, self.y + other.y)
        elif type(other) is tuple:
            return Point2D(self.x + other[0], self.y + other[1])
        elif type(other) is float or int:
            return Point2D(self.x + other, self.y + other)
        else:
            raise ValueError(
                """
                The other parameter should be a instace of Point2D
                or a tuple or a int or a float
                """)

    def __sub__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x - other.x, self.y - other.y)
        elif type(other) is tuple:
            return Point2D(self.x - other[0], self.y - other[1])
        elif type(other) is float or int:
            return Point2D(self.x - other, self.y - other)
        else:
            raise ValueError(
                """
                The other parameter should be a instace of Point2D
                or a tuple or a int or a float
                """)

    def __mul__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x * other.x, self.y * other.y)
        elif type(other) is tuple:
            return Point2D(self.x * other[0], self.y * other[1])
        elif type(other) is float or int:
            return Point2D(self.x * other, self.y * other)
        else:
            raise ValueError(
                """
                The other parameter should be a instace of Point2D
                or a tuple or a int or a float
                """)

    def __truediv__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x / other.x, self.y / other.y)
        elif type(other) is tuple:
            return Point2D(self.x / other[0], self.y / other[1])
        elif type(other) is float or int:
            return Point2D(self.x / other, self.y / other)
        else:
            raise ValueError(
                """
                The other parameter should be a instace of Point2D
                or a tuple or a int or a float
                """)


class Step:
    CONST_DIRECTION_A = 'a'
    CONST_DIRECTION_B = 'b'
    CONST_DIRECTION_C = 'c'
    CONST_DIRECTION_D = 'd'

    def __init__(self, step):
        self.step = step


class Path:
    def __init__(self, *args):
        self.path = []
        for step in args:
            if not isinstance(step, Step):
                raise ValueError('Step should be a instace of Step Class')
            self.path.append(step)

    def get(self, index):
        try:
            return self.path[index]
        except IndexError:
            print('The requested index does not exist in the \'path\' list')
            return None

    def append(self, value):
        if len(self.path) >= 4:
            raise IndexError('The \'path\' list already has 4 elements')
        self.path.append(value)


class Trace:
    def __init__(self, first, second, third, fourth, path):
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
        self.path = path

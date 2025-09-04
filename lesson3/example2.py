class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point {self.x, self.y}"

    def __repr__(self):
        return f"Point {self.x, self.y}"

p1 = Point(1, 2)
p2 = Point(1, 3)
print(p1 == p2)
print(p1)
print(p2)
print(p1 != p2)
points=[p1,p2]
print(points)
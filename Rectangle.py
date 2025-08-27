class Rectangle:
    def __init__(self, width:float, height:float):
        """constructor that accepts the width and height of the rectangle"""
        self.width = width
        self.height = height

    def __str__(self):
        return f'Rectangle(width={self.width}, height={self.height})'

    def area(self):
        """ method that returns the area of the rectangle"""
        return  self.width * self.height

    def perimeter(self):
        """method that returns the perimeter of the rectangle"""
        return 2 * (self.width + self.height)

    def is_square(self):
        """ method that returns True if the rectangle is a square (the width is equal to the height), otherwise False"""
        return self.width == self.height

    def resize(self, new_width, new_height):
        """method that changes the width and height of the rectangle"""
        self.width = new_width
        self.height = new_height

    def describe_rectangle(self):
        """Describe the rectangle"""
        print(self.__str__())
        print(f'area = {self.area()}')
        print(f'perimeter = {self.perimeter()}')
        print(f'This is a square = {self.is_square()}')
        print('\n')
import math

def calculate_circle_area(radius:float)->float:
    """A function that: takes the radius of a circle, and returns the area of the circle."""
    return math.pi * radius ** 2

while True:
    try:
        input_radius = float(input("Enter the radius of the circle: "))
        break
    except ValueError:
        print("Invalid input. Please enter a number!")


area = round(calculate_circle_area(input_radius), 2)
#Result
print(f" The area of a circle with a radius of {input_radius} is {area}")
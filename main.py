#Lesson 1
from Rectangle import Rectangle
from calculate_circle_values import calculate_circle_area

#test
def print_hi(name):
    print(f'Hi, {name}')

if __name__ == '__main__':
    print_hi('PyCharm')

# My check
print("Hello, friend!")

print('------------------ Task Rectangle ------------------')
rec = Rectangle(100, 100)
rec.describe_rectangle()

rec.resize(10, 20)
rec.describe_rectangle()

print('------------------ Task Calculate_circle_area ------------------')
while True:
    try:
        input_radius = float(input("Enter the radius of the circle: "))
        break
    except ValueError:
        print("Invalid input. Please enter a number!")


area = round(calculate_circle_area(input_radius), 2)
#Result
print(f" The area of a circle with a radius of {input_radius} is {area}")
print('------------------ The end ------------------')
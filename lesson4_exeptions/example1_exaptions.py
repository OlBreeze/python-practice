try:
    x = 10 / 10
    print(x)
except ZeroDivisionError as ex:
    print(f"Error: {ex.__class__} - {ex}")
except TypeError as ex:
    print(f"{ex.__class__}: {ex}")
finally:
    print("Finish\n")



variable = 10

try:
	result = f'result of division is: {variable / int(input("enter the divisor: "))}'
except ValueError: # ValueError при введенні не числа
	print('Must be a number')
except ZeroDivisionError: # ZeroDivisionError при введенні 0
	print('Must be a non-zero value')
else:
	print(f'Result is: {result}')
finally:
	print('Thank you!')
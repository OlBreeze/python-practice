class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        real = self.real + other.real
        imag = self.imag + other.imag
        return Complex(real, imag)

    def __str__(self):
        return f"{self.real} + {self.imag}i"


c1 = Complex(1, 2)
c2 = Complex(3, 4)
c3 = c1 + c2  # Викликається __add__
print(c3)  # Виведе: 4 + 6i
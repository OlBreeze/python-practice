class MyMeta(type):
    """rrgrgrgtrg"""
    def __new__(cls, name, bases, dct):
        dct['added_attribute'] = 100
        return super().__new__(cls, name, bases, dct)

class MyNewClass(metaclass=MyMeta):
    def __init__(self, x):
        self.x = x

    def __str__(self):
        return f"Value of: {self.x}"

m_c = MyNewClass(10)
print(m_c)
print(m_c.added_attribute)
print(m_c.__dict__)
print(MyMeta.__dict__)
print(MyNewClass.__dict__)
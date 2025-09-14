class CustomManager:
    def __init__(self, data):
        print("init")
        self.data = data

    def __enter__(self):
        print("enter")
        return "Data from manager"

    def __exit__ (self, exc_type, exc_val, exc_tb):
        print("exit")
        if exc_type:
            print(f"Error: {exc_type}, {exc_val}, {exc_tb}")
            return False

# my_var = CustomManager("test")
with CustomManager("test") as manager:
    print(f"Отримано: {manager}")
    print("End")
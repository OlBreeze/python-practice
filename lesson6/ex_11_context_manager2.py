from contextlib import contextmanager


@contextmanager
def custom_manager():
    print("enter context")
    yield
    print("exit context")


with custom_manager() as c_m:
    print(f"Отримано: {c_m}")

print("End")
#
# Как работает:
#
# При входе в with → выполняется всё до yield → печатает "enter context".
# Внутри with выполняется твой код.
# После выхода → выполняется всё после yield → печатает "exit context".
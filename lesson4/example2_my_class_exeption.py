class TooYoungError(Exception):
    def __init__(self, message="Користувачу менше 18 років"):
        self.message = message
        super().__init__(self.message)

# def verify_age(age):
#     if age < 18:
#         raise TooYoungError("На жаль, Ви занадто молоді для реєстрації.")
#     print("Верифікація успішна! Ласкаво просимо.")


def verify_age(age):
    if not isinstance(age, int):
        raise TypeError("Перевірте тип даних")

    if age < 18:
        raise TooYoungError("На жаль, Ви занадто молоді для реєстрації.")

    print("Верифікація успішна! Ласкаво просимо.")

try:
    verify_age(15)
except TooYoungError as ex:
    print(ex)

# Cntrl + Shift + Alt + U   иерархия класса (эксепшен)
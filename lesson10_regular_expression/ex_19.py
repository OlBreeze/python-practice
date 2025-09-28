# Отримання кількості замін у рядку, в якому відбулася заміна
import re

# string - рядок для пошуку
string = "teSt1 test2 test3 test4 teSt5"

# re.subn(pattern, repl, string, count=0, flags=0)
# pattern - рядок шаблону регулярного виразу,
# repl - рядок заміни,
# count=0 - максимальне число входжень pattern,
# flags=0 - один або декілька прапорців.
result = re.subn(pattern=r"s", repl="x", string=string, flags=re.IGNORECASE)

print(result)

# Функція subn() модуля re виконує ту саму операцію, що й функція sub(), але повертає кортеж
# (new_string, number_of_subs_made), де
# new_string - рядок, отриманий у результаті заміни;
# number_of_subs_made - кількість виконаних замін.
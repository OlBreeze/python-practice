import re

string = 'Test1 Test2 Test3 Test4 Test5'
pattern = "Test"

for match in re.finditer(pattern, string):
    s = "Found '{group}' at {begin}:{end}".format(
        group=match.group(), begin=match.start(),
        end=match.end())
    # Виводимо кожен знайдений результат:
    print(s)
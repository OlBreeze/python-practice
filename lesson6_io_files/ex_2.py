file = open("text.txt", "r", encoding="utf-8")
for line in file:
    print(line)
file.close()
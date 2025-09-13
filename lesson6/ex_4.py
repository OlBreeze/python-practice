with open("text.txt", 'r', encoding="utf-8") as file:
    """data = file.read()
    print(data)"""

    data2 =file.read(15)
    print(data2)

    data3 =file.read(10)
    print(data3)

    data4 =file.readline(5) # одна строка
    print(data4)

    # data5 = file.readlines()
    for line in file:
        print(line)
from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient(host="localhost", port=27017)

# База данных "University"
db = client.University
students = db.students # Коллекция "students"
students.drop()
students_data = [
    {
        "surname": "Іваненко",
        "name": "Іван",
        "age": 20,
        "phone": "+380931112233",
        "email": "ivanenko.ivan@example.com"
    },
    {
        "surname": "Петренко",
        "name": "Марія",
        "age": 19,
        "phone": "+380671234567",
        "email": "petrenko.maria@example.com"
    },
    {
        "surname": "Сидоренко",
        "name": "Олег",
        "age": 21,
        "phone": "+380501112233",
        "email": "sydorenko.oleg@example.com"
    },
    {
        "surname": "Коваленко",
        "name": "Анна",
        "age": 22,
        "phone": "+380931234555",
        "email": "kovalenko.anna@example.com"
    },
    {
        "surname": "Бондаренко",
        "name": "Дмитро",
        "age": 20,
        "phone": "+380671118899",
        "email": "bondarenko.dmytro@example.com"
    }
]

# Вставка данных
result = students.insert_many(students_data)
print(f"Inserted {len(result.inserted_ids)} students")

for student in students.find():
    print(student)

# print(students)
total = students.count_documents({})
print(f"Всього студентів: {total}")
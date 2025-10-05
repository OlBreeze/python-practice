from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017)

db = client.University
students = db.students
for student in students.find():
    print(student)

# print(students)
total = students.count_documents({})
print(f"Всього студентів: {total}")

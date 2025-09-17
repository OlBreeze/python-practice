import json

data = {
    "name": "Ivan",
    "age": 22,
    "hobbies": ["python", "programming"],
}

print(json.dumps(data))
print(type(json.dumps(data)))
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

with open("data.json", "r") as f:
    data = json.load(f)
    print(data)
    print(type(data))

test_data = """
    {
    "name": "Ivan",
    "age": 22,
    "hobbies": ["python1", "programming1"]
    }
"""
print(json.loads(test_data))
print(type(json.loads(test_data)))
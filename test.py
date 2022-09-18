import json

with open('index.json', 'r') as f:
    data = json.load(f)
    print(type(data))
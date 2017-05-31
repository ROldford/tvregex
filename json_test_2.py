import json

FILENAME = "test_file.json"
shownames_dict = {}

with open(FILENAME) as f:
    shownames_dict = json.load(f)
    print(shownames_dict)

print(shownames_dict["atmidnight"])

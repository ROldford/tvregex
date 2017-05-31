import json


SHOWNAMES_DICT = {
    "lipsyncbattle": "Lip Sync Battle",
    "archer2009": "Archer (2009)",
    "thedailyshow": "The Daily Show",
    "atmidnight": "@midnight"
}

with open("test_file.json", "w") as f:
    json.dump(SHOWNAMES_DICT, f, indent=4)

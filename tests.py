import json
from main import *

with open("mocks.json", "r") as f:
    data_json = json.load(f)

for data_enum in data_json["enums"]:
    createEnum(data_enum)

for data_entity in data_json["entities"]:
    createEntity(data_entity)

init()
generateFiles()
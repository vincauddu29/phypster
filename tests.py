import json
from main import *

with open("mocks.json", "r") as f:
    data_json = json.load(f)

for data_entity in data_json["entities"]:
    createEntity(data_entity)

init()
generateFiles()

from Tests.Mocks.AdressMock import AdressMock
from src.DTOs.AdressDTO import AdressDTO
from src.Models.AdressEntity import AdressEntity

# from Tests.Ressources.test_AdressRessourceTest import AdressRessourceTest

# a = AdressRessourceTest()

# a.test_getAll_empty()

mock = AdressMock()

# dto = AdressDTO()

a = mock.createEntityWithoutRelationship()
a2 = mock.createEntityWithRelationship()

# print(dto.dump(a))
# print(dto.dump(a2))
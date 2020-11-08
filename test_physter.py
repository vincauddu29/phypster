import json
from phypster import Phypster
from unittest import TestCase

class PhypsterTest(TestCase):
        # with open("mocks.json", "r") as f:
        #     data_json = json.load(f)

        # for data_enum in data_json["enums"]:
        #     createEnum(data_enum)

        # for data_entity in data_json["entities"]:
        #     createEntity(data_entity)

        # init()
        # generateFiles()

    def setUp(self):
        self.phypster = Phypster()

    def test_init(self):
        assert len(self.phypster.ASSOCIATETABLES) == 0
        assert len(self.phypster.ENTITIES) == 0
        assert len(self.phypster.ENUMS) == 0

    def test_createEnum(self):
        data_enum = {
            "name": "Genre",
            "listItems": [
                "Homme",
                "Femme"
            ]
        }

        self.phypster.createEnum(data_enum)

        assert len(self.phypster.ENUMS) == 1
        enum = self.phypster.ENUMS['Genre']

        assert enum.nameEnum == "Genre"
        assert len(enum.listItems) == 2
        assert enum.listItems[0] == "Homme"
        assert enum.listItems[1] == "Femme"

    def test_createTwoEnums(self):
        data_enum1 = {
            "name": "Genre",
            "listItems": [
                "Homme",
                "Femme"
            ]
        }
        data_enum2 = {
            "name": "TypeData",
            "listItems": [
                "Int",
                "Str"
                "Datetime",
                "Boolean"
            ]
        }

        self.phypster.createEnum(data_enum1)
        self.phypster.createEnum(data_enum2)

        assert len(self.phypster.ENUMS) == 2
        assert 'TypeData' in self.phypster.ENUMS.keys()
        assert 'Genre' in self.phypster.ENUMS.keys()

    def test_createEntityWithoutRelationship(self):
        data_entity = {
            "name": "Entity1",
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [],
            "enums": [
            ]
        }

        self.phypster.createEntity(data_entity)

        entity = self.phypster.ENTITIES["Entity1"]
        pk = entity.getPrimaryKey()

        assert len(self.phypster.ENTITIES) == 1
        assert entity.nameEntity == "Entity1"
        assert len(entity.columns) == 2
        assert len(entity.relationships) == 0
        assert len(entity.enums) == 0
        assert pk != None
        assert pk.nameColumn == "id"

    def test_createEntityOneToOne(self):
        nameEntity1 = "Entity3"
        nameEntity2 = "Entity4"
        data_entities = [{
            "name": nameEntity1,
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [],
            "enums": []
        },{
            "name": nameEntity2,
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [
                {
                    "entity2": nameEntity1,
                    "typeRelation": "One to One"
                }
            ],
            "enums": []
        }]
        self.phypster.createEntity(data_entities[0])
        self.phypster.createEntity(data_entities[1])

        assert len(self.phypster.ENTITIES) == 2

        e1 = self.phypster.ENTITIES[nameEntity1]
        e2 = self.phypster.ENTITIES[nameEntity2]

        assert len(e1.relationships) == 1
        assert len(e2.relationships) == 1

        e1_r1 = e1.relationships[0]
        e2_r1 = e2.relationships[0]

        assert e1_r1.entity1.nameEntity == nameEntity2
        assert e1_r1.entity2.nameEntity == nameEntity1
        assert e2_r1.entity1.nameEntity == nameEntity2
        assert e2_r1.entity2.nameEntity == nameEntity1

        assert e1_r1.isOneToOne == True
        assert e1_r1.isManyToOne == False
        assert e1_r1.isOneToMany == False
        assert e1_r1.isManyToMany == False

        assert e2_r1.isOneToOne == True
        assert e2_r1.isManyToOne == False
        assert e2_r1.isOneToMany == False
        assert e2_r1.isManyToMany == False

        assert len(self.phypster.ASSOCIATETABLES) == 0

    def test_createEntityManyToOne(self):
        nameEntity1 = 'Entity5'
        nameEntity2 = 'Entity6'
        data_entities = [{
            "name": nameEntity1,
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [],
            "enums": []
        },{
            "name": nameEntity2,
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [
                {
                    "entity2": nameEntity1,
                    "typeRelation": "Many to One"
                }
            ],
            "enums": []
        }]
        self.phypster.createEntity(data_entities[0])
        self.phypster.createEntity(data_entities[1])

        assert len(self.phypster.ENTITIES) == 2

        e1 = self.phypster.ENTITIES[nameEntity1]
        e2 = self.phypster.ENTITIES[nameEntity2]

        assert len(e1.relationships) == 1
        assert len(e2.relationships) == 1

        e1_r1 = e1.relationships[0]
        e2_r1 = e2.relationships[0]

        assert e1_r1.entity1.nameEntity == nameEntity2
        assert e1_r1.entity2.nameEntity == nameEntity1
        assert e2_r1.entity1.nameEntity == nameEntity2
        assert e2_r1.entity2.nameEntity == nameEntity1

        assert e1_r1.isOneToOne == False
        assert e1_r1.isManyToOne == True
        assert e1_r1.isOneToMany == False
        assert e1_r1.isManyToMany == False

        assert e2_r1.isOneToOne == False
        assert e2_r1.isManyToOne == True
        assert e2_r1.isOneToMany == False
        assert e2_r1.isManyToMany == False

        assert len(self.phypster.ASSOCIATETABLES) == 0

    def test_createEntityOneToMany(self):
        nameEntity1 = 'Entity7'
        nameEntity2 = 'Entity8'
        data_entities = [{
            "name": nameEntity1,
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [],
            "enums": []
        },{
            "name": nameEntity2,
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [
                {
                    "entity2": nameEntity1,
                    "typeRelation": "One to Many"
                }
            ],
            "enums": []
        }]
        self.phypster.createEntity(data_entities[0])
        self.phypster.createEntity(data_entities[1])

        assert len(self.phypster.ENTITIES) == 2

        e1 = self.phypster.ENTITIES[nameEntity1]
        e2 = self.phypster.ENTITIES[nameEntity2]

        assert len(e1.relationships) == 1
        assert len(e2.relationships) == 1

        e1_r1 = e1.relationships[0]
        e2_r1 = e2.relationships[0]

        assert e1_r1.entity1.nameEntity == nameEntity2
        assert e1_r1.entity2.nameEntity == nameEntity1
        assert e2_r1.entity1.nameEntity == nameEntity2
        assert e2_r1.entity2.nameEntity == nameEntity1

        assert e1_r1.isOneToOne == False
        assert e1_r1.isManyToOne == False
        assert e1_r1.isOneToMany == True
        assert e1_r1.isManyToMany == False

        assert e2_r1.isOneToOne == False
        assert e2_r1.isManyToOne == False
        assert e2_r1.isOneToMany == True
        assert e2_r1.isManyToMany == False

        assert len(self.phypster.ASSOCIATETABLES) == 0

    def test_createEntityManyToMany(self):
        nameEntity1 = 'Entity9'
        nameEntity2 = 'Entity10'
        data_entities = [{
            "name": nameEntity1,
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [],
            "enums": []
        },{
            "name": nameEntity2,
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [
                {
                    "entity2": nameEntity1,
                    "typeRelation": "Many to Many"
                }
            ],
            "enums": []
        }]
        self.phypster.createEntity(data_entities[0])
        self.phypster.createEntity(data_entities[1])

        assert len(self.phypster.ENTITIES) == 2

        e1 = self.phypster.ENTITIES[nameEntity1]
        e2 = self.phypster.ENTITIES[nameEntity2]

        assert len(e1.relationships) == 1
        assert len(e2.relationships) == 1

        e1_r1 = e1.relationships[0]
        e2_r1 = e2.relationships[0]

        assert e1_r1.entity1.nameEntity == nameEntity2
        assert e1_r1.entity2.nameEntity == nameEntity1
        assert e2_r1.entity1.nameEntity == nameEntity2
        assert e2_r1.entity2.nameEntity == nameEntity1

        assert e1_r1.isOneToOne == False
        assert e1_r1.isManyToOne == False
        assert e1_r1.isOneToMany == False
        assert e1_r1.isManyToMany == True

        assert e2_r1.isOneToOne == False
        assert e2_r1.isManyToOne == False
        assert e2_r1.isOneToMany == False
        assert e2_r1.isManyToMany == True

        assert len(self.phypster.ASSOCIATETABLES) == 1

    def test_createEntityWithEnumNullable(self):
        data_enum = {
            "name": "TypeData",
            "listItems": [
                "Int",
                "Str"
                "Datetime",
                "Boolean"
            ]
        }

        self.phypster.createEnum(data_enum)

        data_entity = {
            "name": "Entity1",
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [],
            "enums": [
                {
                    "name": "TypeData",
                    "nullable": True
                }
            ]
        }

        self.phypster.createEntity(data_entity)

        assert len(self.phypster.ENTITIES['Entity1'].enums) == 1

        enum = self.phypster.ENTITIES['Entity1'].enums[0]
        assert enum.nullable == True
        assert enum.enum.nameEnum == "TypeData"

    def test_createEntityWithEnumNotNullable(self):
        data_enum = {
            "name": "TypeData",
            "listItems": [
                "Int",
                "Str"
                "Datetime",
                "Boolean"
            ]
        }

        self.phypster.createEnum(data_enum)

        data_entity = {
            "name": "Entity1",
            "columns": [
                ["col1", "Float", False, False],
                ["col2", "DateTime", False, False]
            ],
            "relationships": [],
            "enums": [
                {
                    "name": "TypeData",
                    "nullable": False
                }
            ]
        }

        self.phypster.createEntity(data_entity)

        assert len(self.phypster.ENTITIES['Entity1'].enums) == 1

        enum = self.phypster.ENTITIES['Entity1'].enums[0]
        assert enum.nullable == False
        assert enum.enum.nameEnum == "TypeData"
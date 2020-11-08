#!/usr/bin/python3
import os, inquirer, shutil, json
from typing import Dict, List
from distutils.sysconfig import get_python_lib
from jinja2 import Template
import argparse

from Entity import *

class Phypster:
    def __init__(self):
        self.DEBUG = False
        self.ASSOCIATETABLES: List[AssociateTable] = []
        self.ENTITIES: Dict[str, Entity] = dict()
        self.ENUMS: Dict[str, EnumEntity] = dict()

    def log(self, message: str, type_message = "DEBUG"):
        if type_message == "INFO":
            print(message)
        elif type_message == "ERROR":
            print(message)
        else:
            if self.DEBUG:
                print(message)

    # define our clear function 
    def clear(self, ):
        # for windows 
        if os.name == 'nt': 
            _ = os.system('cls') 
    
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = os.system('clear') 

    def info(self, message: str):
        self.log(message, "INFO")

    def error(self, message: str):
        self.log(message, "ERROR")

    def debug(self, message: str):
        self.log(message)

    def createDirectory(self, name: str):
        if not os.path.exists(name):
            os.mkdir(name)
            self.info("[x] {0} directory created".format(name))
            open("{0}/__init__.py".format(name), "w").close()
            self.info("[x] {0}/__init__.py created".format(name))
        else:
            self.info("[x] {0} directory skip".format(name))

    def getPathFileInStatic(self, path: str):
        BASE_DIR = None

        if os.path.isfile(get_python_lib() + "/phypster"):
            BASE_DIR = get_python_lib() + "/phypster"
        else:
            BASE_DIR = os.getcwd()

        self.debug("BASE_DIR = {0}".format(BASE_DIR))

        return BASE_DIR + "/static/" + path

    def init(self):
        """ Init a new project """

        # create directories
        self.createDirectory("src")
        list_directories_name = {
            "Models": True,
            "DTOs": True,
            "Repositories": True,
            "Services": True,
            "Mappeurs": True,
            "Ressources": True,
            "Logs": False,
            "Parsers": False,
            "docker": False,
            "Enums": False,
            "Config": False,
        }

        for directory_name in list_directories_name:
            self.createDirectory("src/" + directory_name)

        self.createDirectory("src/Logs")
        open("src/Logs/debug.log", "w").close()
        open("src/Logs/info.log", "w").close()
        open("src/Logs/error.log", "w").close()

        # test directories
        self.createDirectory("Tests")
        for directory_name in list_directories_name.keys():
            if list_directories_name[directory_name]:
                self.createDirectory("Tests/" + directory_name)

        # helpers Test
        shutil.copy(self.getPathFileInStatic("helpersTest.py"), "Tests/helpersTest.py")

        # Security config
        shutil.copy(self.getPathFileInStatic("security.py"), "src/Config/SecurityConfig.py")

        # Logger
        shutil.copy(self.getPathFileInStatic("logger.py"), "src/Config/Logger.py")

        self.createDirectory("Tests/Mocks")

        self.writeAppFile()

        shutil.copy(self.getPathFileInStatic("config.py"), "src/Config/ApplicationConfig.py")
        self.info("[x] create config.py")
        # shutil.copy(getPathFileInStatic("__init__.py"), "src/__init__.py")
        # info("[x] create __init__.py")
        shutil.copy(self.getPathFileInStatic("server.py"), "server.py")
        self.info("[x] create server.py")
        shutil.copy(self.getPathFileInStatic("docker-compose.test.yml"), "src/docker/docker-compose.test.yml")
        self.info("[x] create docker-compose.test.yml")

    def createEntity(self, data = None):
        cond_stop = False

        if data == None:
            data = {"columns": [], "relationships": [], "enums": []}
            self.clear()
            name_question = [inquirer.Text('name', message="What's the entity name")]
            name_answer = inquirer.prompt(name_question)

            data["name"] = name_answer['name']

            choose_step = [inquirer.List('choose', message="What now", choices=['Column', 'RelationShip', 'Stop'])]

            while not cond_stop:
                self.clear()
                step_answer = inquirer.prompt(choose_step)

                if step_answer['choose'] == 'Stop':
                    cond_stop = True
                elif step_answer['choose'] == 'Column':
                    questions = [
                        inquirer.Text('name', message="What's the column name"),
                        inquirer.List('typeData', message="What is the data type", choices=['Integer', 'String', 'Float', 'DateTime', 'Boolean', 'Enum']),
                    ]
                    self.clear()
                    answers = inquirer.prompt(questions)
                    if answers["typeData"] == "enum":
                        enums_name = list(self.ENUMS.keys())
                        enum_question = [inquirer.List('enum', message="What's the enum", choices=enums_name)]
                        self.clear()
                        enum_answer = inquirer.prompt(enum_question)

                    attribute_question = [
                        inquirer.Checkbox('attr', message="Choose attributes", choices=['Primary Key', 'Nullable'])
                    ]
                    self.clear()
                    attribute_answer = inquirer.prompt(attribute_question)
                    nullable = True if 'Nullable' in attribute_answer['attr'] else False
                    primaryKey = True if 'Primary Key' in attribute_answer['attr'] else False

                    if answers["typeData"] != "enum":
                        data["columns"].append([attribute_answer["name"], attribute_answer["typeData"], primaryKey, nullable])
                    else:
                        enums_name = list(self.ENUMS.keys())
                        data["enums"].append({"name" : enum_answer["enum"], "nullable": nullable, "primaryKey": primaryKey})

                else:
                    entities_name = list(self.ENTITIES.keys())
                    entities_name.append('Back')
                    relation_question = [
                        inquirer.List('typeRelation', message="What's the relation", choices=['One to One', 'One to Many', 'Many to One', 'Many to Many', 'Back']),
                        inquirer.List('entity', message="What's the entity", choices=entities_name)
                    ]
                    self.clear()
                    relation_answer = inquirer.prompt(relation_question)

                    relationship_data = dict()
                    relationship_data["entity2"] = relation_answer['entity']
                    relationship_data["typeRelation"] = relation_answer['typeRelation']

                    data["relationships"].append(relationship_data)

        entity = Entity(data["name"])

        for data_column in data["columns"]:
            entity.addColumn(data_column[0], data_column[1], data_column[2], data_column[3])

        for data_relationship in data["relationships"]:
            # retrieve the second entity
            entity2 = self.ENTITIES[data_relationship["entity2"]]

            if data_relationship['typeRelation'] == 'One to One':
                relationship = RelationShip(entity, entity2, isOneToOne=True)
            elif data_relationship['typeRelation'] == 'Many to One':
                relationship = RelationShip(entity, entity2, isManyToOne=True)
            elif data_relationship['typeRelation'] == 'One to Many':
                relationship = RelationShip(entity, entity2, isOneToMany=True)
            elif data_relationship['typeRelation'] == 'Many to Many':
                associate = AssociateTable(entity, entity2)
                relationship = RelationShip(entity, entity2, isManyToMany=True, associateTable=associate)
                self.ASSOCIATETABLES.append(associate)
            else:
                pass

            entity.addRelationShip(relationship)
            entity2.addRelationShip(relationship)
            self.ENTITIES[entity2.nameEntity] = entity2

        for data_enum in data["enums"]:
            entity.addEnum(self.ENUMS[data_enum["name"]], data_enum["nullable"])

        self.ENTITIES[data['name']] = entity

    def createEnum(self, data = None):
        if data == None:
            data = {"listItems": []}
            cond_stop = False
            self.clear()
            name_question = [inquirer.Text('name', message="What's the entity name")]
            name_answer = inquirer.prompt(name_question)
            data["name"] = name_answer["name"]
            

            choose_step = [inquirer.List('choose', message="What now", choices=['Add item into the enum', 'Stop'])]

            while not cond_stop:
                self.clear()
                step_answer = inquirer.prompt(choose_step)

                if step_answer['choose'] == 'Stop':
                        cond_stop = True
                elif step_answer['choose'] == 'Add item into the enum':
                    questions = [inquirer.Text('name', message="What's the item name")]
                    self.clear()
                    answers = inquirer.prompt(questions)
                    data.listItems.append(answers["name"])

        enum = EnumEntity(data["name"])
        for item in data["listItems"]:
            enum.addItem(item)

        self.ENUMS[enum.nameEnum] = enum

    def writeFile(self, path_template, path_output, entity):
        # Open template
        with open(self.getPathFileInStatic(path_template)) as f:
            template = Template(f.read())
        data = template.render(entity=entity)

        # Write file into the directory
        with open(path_output, "w") as f:
            f.write(data)

    def writeAppFile(self, ):
        # Open template
        with open(self.getPathFileInStatic("template/app.py.j2")) as f:
            template = Template(f.read())
        data = template.render(entities=list(self.ENTITIES.values()))

        # Write file into the directory
        # with open("src/app.py", "w") as f:

        with open("src/__init__.py", "w") as f:
            f.write(data)
            self.info("[x] create (or updated) __init__.py")

    def generateEntitiesFiles(self, entity):
        self.writeFile("template/entity.py.j2", "src/Models/{0}Entity.py".format(entity.nameEntity), entity)
        self.info("[x] {0}Entity file created".format(entity.nameEntity))

    def generateRepositoriesFiles(self, entity):
        self.writeFile("template/repository.py.j2", "src/Repositories/{0}Repository.py".format(entity.nameEntity), entity)
        self.info("[x] {0}Repository file created".format(entity.nameEntity))

    def generateDTOsFiles(self, entity):
        self.writeFile("template/dtoV1.py.j2", "src/DTOs/{0}DTO.py".format(entity.nameEntity), entity)
        self.info("[x] {0}DTO file created".format(entity.nameEntity))

    def generateMappeursFiles(self, entity):
        self.writeFile("template/mappeur.py.j2", "src/Mappeurs/{0}Mappeur.py".format(entity.nameEntity), entity)
        self.info("[x] {0}Mappeur file created".format(entity.nameEntity))

    def generateServicesFiles(self, entity):
        self.writeFile("template/service.py.j2", "src/Services/{0}Service.py".format(entity.nameEntity), entity)
        self.info("[x] {0}Service file created".format(entity.nameEntity))

    def generateAssociatedTableFiles(self, associatedTable):
        self.writeFile("template/associatedTable.py.j2", "src/Models/{0}.py".format(associatedTable.name), associatedTable)
        self.info("[x] {0} file created".format(associatedTable.name))

    def generateParsersFiles(self, entity):
        self.writeFile("template/parser.py.j2", "src/Parsers/{0}Parser.py".format(entity.nameEntity), entity)
        self.info("[x] {0}Parser file created".format(entity.nameEntity))

    def generateRessourcesFiles(self, entity):
        self.writeFile("template/ressource.py.j2", "src/Ressources/{0}Ressource.py".format(entity.nameEntity), entity)
        self.info("[x] {0}Ressource file created".format(entity.nameEntity))

    def generateEnumsFiles(self, entity):
        self.writeFile("template/enum.py.j2", "src/Enums/{0}Enum.py".format(entity.nameEnum), entity)
        self.info("[x] {0}Enum file created".format(entity.nameEnum))

    # TESTS
    def generateEntitiesTestsFiles(self, entity):
        self.writeFile("template/entityTest.py.j2", "Tests/Models/test_{0}EntityTest.py".format(entity.nameEntity), entity)
        self.info("[x] {0}EntityTest file created".format(entity.nameEntity))

    def generateDTOsTestsFiles(self, entity):
        self.writeFile("template/dtoV1Test.py.j2", "Tests/DTOs/test_{0}DTOTest.py".format(entity.nameEntity), entity)
        self.info("[x] {0}DTOTest file created".format(entity.nameEntity))

    def generateMappeursTestsFiles(self, entity):
        self.writeFile("template/mappeurTest.py.j2", "Tests/Mappeurs/test_{0}MappeurTest.py".format(entity.nameEntity), entity)
        self.info("[x] {0}MappeurTest file created".format(entity.nameEntity))

    def generateRessourcesTestsFiles(self, entity):
        self.writeFile("template/ressourceTest.py.j2", "Tests/Ressources/test_{0}RessourceTest.py".format(entity.nameEntity), entity)
        self.info("[x] {0}RessourceTest file created".format(entity.nameEntity))

    def generateRepositoriesTestsFiles(self, entity):
        self.writeFile("template/repositoryTest.py.j2", "Tests/Repositories/test_{0}RepositoryTest.py".format(entity.nameEntity), entity)
        self.info("[x] {0}RepositoryTest file created".format(entity.nameEntity))

    def generateServicesTestsFiles(self, entity):
        self.writeFile("template/serviceTest.py.j2", "Tests/Services/test_{0}ServiceTest.py".format(entity.nameEntity), entity)
        self.info("[x] {0}ServiceTest file created".format(entity.nameEntity))

    def generateMocksTestsFiles(self, entity):
        self.writeFile("template/mock.py.j2", "Tests/Mocks/{0}Mock.py".format(entity.nameEntity), entity)
        self.info("[x] {0}Mock file created".format(entity.nameEntity))

    def generateFiles(self):
        for name in self.ENTITIES.keys():
            entity = self.ENTITIES[name]
            self.generateEntitiesFiles(entity)
            self.generateRepositoriesFiles(entity)
            self.generateDTOsFiles(entity)
            self.generateMappeursFiles(entity)
            self.generateServicesFiles(entity)
            self.generateParsersFiles(entity)
            self.generateRessourcesFiles(entity)

            # tests
            self.generateEntitiesTestsFiles(entity)
            self.generateDTOsTestsFiles(entity)
            self.generateMappeursTestsFiles(entity)
            # self.generateRessourcesTestsFiles(entity)
            self.generateRepositoriesTestsFiles(entity)
            self.generateServicesTestsFiles(entity)
            self.generateMocksTestsFiles(entity)

        for associateTable in self.ASSOCIATETABLES:
            self.generateAssociatedTableFiles(associateTable)

        for enum in self.ENUMS.values():
            self.generateEnumsFiles(enum)

        self.writeAppFile()

#############
# argsparse #
#############
parser = argparse.ArgumentParser(description='Flask starter')
parser.add_argument('--import_json', help='import json model')

args = parser.parse_args()

phypster = Phypster()

if __name__ == "__main__":
    if args.import_json != None:
        with open("mocks.json", "r") as f:
            data_json = json.load(f)

        for data_enum in data_json["enums"]:
            phypster.createEnum(data_enum)

        for data_entity in data_json["entities"]:
            phypster.createEntity(data_entity)
    else:
        cond_stop = False
        choose_step = [inquirer.List('choose', message="What now", choices=['Create entity', 'Create enum', 'Stop'])]

        while not cond_stop:
            step_answer = inquirer.prompt(choose_step)

            if step_answer['choose'] == 'Create entity':
                phypster.createEntity()
            elif step_answer['choose'] == 'Create enum':
                phypster.createEnum()
            else:
                cond_stop = True
    phypster.init()
    phypster.generateFiles()
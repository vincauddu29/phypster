#!/usr/bin/python3
import os
import inquirer
import shutil
import json
from typing import Dict, List
from distutils.sysconfig import get_python_lib
from jinja2 import Template
import setuptools as _
from .Entity import AssociateTable, EnumEntity, Entity, RelationShip


class Phypster:
    def __init__(self):
        self.DEBUG = False
        self.ASSOCIATETABLES: List[AssociateTable] = []
        self.ENTITIES: Dict[str, Entity] = dict()
        self.ENUMS: Dict[str, EnumEntity] = dict()
        with open("configFiles.json") as f:
            self.CONFIG_FILES = json.load(f)

    def log(self, message: str, type_message="DEBUG"):
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
            open("{0}{1}__init__.py".format(name, os.sep), "w").close()
            self.info("[x] {0}{1}__init__.py created".format(name, os.sep))
        else:
            self.info("[x] {0} directory skip".format(name))

    def getPathFileInStatic(self, path: str):
        BASE_DIR = None

        pathSitePackageUser = os.sep.join(_.__path__[0].split(os.sep)[:-1])

        if os.path.exists(pathSitePackageUser + os.sep + "phypster"):
            BASE_DIR = pathSitePackageUser + os.sep + "phypster"
        elif os.path.isfile(get_python_lib() + os.sep + "phypster"):
            BASE_DIR = get_python_lib() + os.sep + "phypster"
        else:
            BASE_DIR = os.getcwd()

        return BASE_DIR + os.sep + "static" + os.sep + path

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

        for pathsConfig in self.CONFIG_FILES["staticFiles"]:
            path = self.getPathFileInStatic(pathsConfig["pathInput"])
            shutil.copy(path, pathsConfig["pathOutput"])
            if pathsConfig["postCreateCmd"] != "":
                os.system(pathsConfig["postCreateCmd"])
            self.debug("[x] {0} file created".format(pathsConfig["pathOutput"]))
        

        self.writeAppFile()

    def generateEntityData(self):
        cond_stop = False
        data = {"columns": [], "relationships": [], "enums": []}
        self.clear()
        name_question = [
            inquirer.Text(
                'name',
                message="What's the entity name"
                )]
        name_answer = inquirer.prompt(name_question)

        data["name"] = name_answer['name']

        choose_step = [
            inquirer.List(
                'choose',
                message="What now",
                choices=[
                    'Column',
                    'RelationShip',
                    'Stop'
                ]
            )
        ]

        while not cond_stop:
            self.clear()
            step_answer = inquirer.prompt(choose_step)

            if step_answer['choose'] == 'Stop':
                cond_stop = True
            elif step_answer['choose'] == 'Column':
                questions = [
                    inquirer.Text(
                        'name',
                        message="What's the column name"
                    ),
                    inquirer.List(
                        'typeData',
                        message="What is the data type",
                        choices=[
                            'Integer',
                            'String',
                            'Float',
                            'DateTime',
                            'Boolean',
                            'Enum'
                        ]),
                ]
                self.clear()
                answers = inquirer.prompt(questions)
                if answers["typeData"] == "enum":
                    enums_name = list(self.ENUMS.keys())
                    enum_question = [
                        inquirer.List(
                            'enum',
                            message="What's the enum",
                            choices=enums_name
                        )
                    ]
                    self.clear()
                    enum_answer = inquirer.prompt(enum_question)

                attribute_question = [
                    inquirer.Checkbox(
                        'attr',
                        message="Choose attributes",
                        choices=['Primary Key', 'Nullable']
                    )
                ]
                self.clear()
                attribute_answer = inquirer.prompt(attribute_question)
                nullable = True if 'Nullable' in attribute_answer['attr'] else False
                primaryKey = True if 'Primary Key' in attribute_answer['attr'] else False

                if answers["typeData"] != "enum":
                    data["columns"].append([attribute_answer["name"], attribute_answer["typeData"], primaryKey, nullable])
                else:
                    enums_name = list(self.ENUMS.keys())
                    data["enums"].append({"name": enum_answer["enum"], "nullable": nullable, "primaryKey": primaryKey})

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

        return data

    def createEntity(self, data=None):
        entity = Entity(data["name"])

        for data_column in data["columns"]:
            entity.addColumn(data_column["name"], data_column["type"], data_column["primary"], data_column["nullable"])

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

    def generateEnumData(self):
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
        return data

    def createEnum(self, data=None):
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

    def generateFiles(self, entity: Entity, pathStaticFile: str, pathOutput: str):
        self.writeFile(pathStaticFile, pathOutput.format(entity.nameEntity), entity)
        self.debug("[x] {0} file created".format(pathOutput))

    def generateEnumsFiles(self, entity):
        self.writeFile("template/enum.py.j2", "src/Enums/{0}Enum.py".format(entity.nameEnum), entity)
        self.debug("[x] {0}Enum file created".format(entity.nameEnum))

    def generateAssociatedTableFiles(self, associatedTable):
        self.writeFile("template/associatedTable.py.j2", "src/Models/{0}.py".format(associatedTable.name), associatedTable)
        self.info("[x] {0} file created".format(associatedTable.name))

    def generateFiles(self):
        entityfilesPaths = self.CONFIG_FILES["entityFiles"]
        for name in self.ENTITIES.keys():
            entity = self.ENTITIES[name]
            for paths in entityfilesPaths:
                self.generateFiles(entity, paths["pathInput"], paths["pathOutput"])

        for associateTable in self.ASSOCIATETABLES:
            self.generateAssociatedTableFiles(associateTable)

        for enum in self.ENUMS.values():
            self.generateEnumsFiles(enum)

        self.writeAppFile()

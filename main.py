import os, inquirer
import shutil
from distutils.sysconfig import get_python_lib
from jinja2 import Template

from Entity import *

DEBUG = False
ENTITIES = dict()
ASSOCIATETABLES = []

def log(message: str, type_message = "DEBUG"):
    if type_message == "INFO":
        print(message)
    elif type_message == "ERROR":
        print(message)
    else:
        if DEBUG:
            print(message)

# define our clear function 
def clear():
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

def info(message: str):
    log(message, "INFO")

def error(message: str):
    log(message, "ERROR")

def debug(message: str):
    log(message)

def createDirectory(name: str):
    if not os.path.exists(name):
        os.mkdir(name)
        info("[x] {0} directory created".format(name))
        open("{0}/__init__.py".format(name), "w").close()
        info("[x] {0}/__init__.py created".format(name))
    else:
        info("[x] {0} directory skip".format(name))

def getPathFileInStatic(path: str):
    BASE_DIR = None

    if os.path.isfile(get_python_lib() + "/phypster"):
        BASE_DIR = get_python_lib() + "/phypster"
    else:
        BASE_DIR = os.getcwd()

    debug("BASE_DIR = {0}".format(BASE_DIR))

    return BASE_DIR + "/static/" + path

def init():
    """ Init a new project """

    # create directories
    createDirectory("src")
    list_directories_name = {
        "Models": True,
        "DTOs": True,
        "Repositories": True,
        "Services": True,
        "Mappeurs": True,
        "Ressources": True,
        "Logs": False,
        "Parsers": False,
        "docker": False
    }

    for directory_name in list_directories_name:
        createDirectory("src/" + directory_name)

    createDirectory("src/Logs")
    open("src/Logs/debug.log", "w").close()
    open("src/Logs/info.log", "w").close()
    open("src/Logs/error.log", "w").close()
    open("src/Logs/critic.log", "w").close()

    # test directories
    createDirectory("Tests")
    for directory_name in list_directories_name.keys():
        if list_directories_name[directory_name]:
            createDirectory("Tests/" + directory_name)

    # helpers Test
    shutil.copy(getPathFileInStatic("helpersTest.py"), "Tests/helpersTest.py")

    createDirectory("Tests/Mocks")

    writeAppFile()

    shutil.copy(getPathFileInStatic("config.py"), "src/config.py")
    info("[x] create config.py")
    # shutil.copy(getPathFileInStatic("__init__.py"), "src/__init__.py")
    # info("[x] create __init__.py")
    shutil.copy(getPathFileInStatic("server.py"), "server.py")
    info("[x] create server.py")
    shutil.copy(getPathFileInStatic("docker-compose.test.yml"), "src/docker/docker-compose.test.yml")
    info("[x] create docker-compose.test.yml")

def createEntity(data = None):
    cond_stop = False

    if data == None:
        data = {"columns": [], "relationships": []}
        clear()
        name_question = [inquirer.Text('name', message="What's the entity name")]
        name_answer = inquirer.prompt(name_question)

        data["name"] = name_answer['name']

        choose_step = [inquirer.List('choose', message="What now", choices=['Column', 'RelationShip', 'Stop'])]

        while not cond_stop:
            clear()
            step_answer = inquirer.prompt(choose_step)

            if step_answer['choose'] == 'Stop':
                cond_stop = True
            elif step_answer['choose'] == 'Column':
                questions = [
                    inquirer.Text('name', message="What's the column name"),
                    inquirer.List('typeData', message="What is the data type", choices=['Integer', 'String', 'Float', 'DateTime', 'Boolean']),
                    inquirer.Checkbox('attr', message="Choose attributes", choices=['Primary Key', 'Nullable'])
                ]
                clear()
                answers = inquirer.prompt(questions)
                nullable = True if 'Nullable' in answers['attr'] else False
                primaryKey = True if 'Primary Key' in answers['attr'] else False
                data["columns"].append([answers["name"], answers["typeData"], primaryKey, nullable])
            else:
                entities_name = list(ENTITIES.keys())
                entities_name.append('Back')
                relation_question = [
                    inquirer.List('typeRelation', message="What's the relation", choices=['One to One', 'One to Many', 'Many to One', 'Many to Many', 'Back']),
                    inquirer.List('entity', message="What's the entity", choices=entities_name)
                ]
                clear()
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
        entity2 = ENTITIES[data_relationship["entity2"]]

        if data_relationship['typeRelation'] == 'One to One':
            relationship = RelationShip(entity, entity2, isOneToOne=True)
        elif data_relationship['typeRelation'] == 'Many to One':
            relationship = RelationShip(entity, entity2, isManyToOne=True)
        elif data_relationship['typeRelation'] == 'One to Many':
            relationship = RelationShip(entity, entity2, isOneToMany=True)
        elif data_relationship['typeRelation'] == 'Many to Many':
            associate = AssociateTable(entity, entity2)
            relationship = RelationShip(entity, entity2, isManyToMany=True, associateTable=associate)
            ASSOCIATETABLES.append(associate)
        else:
            pass

        entity.addRelationShip(relationship)
        entity2.addRelationShip(relationship)
        ENTITIES[entity2.nameEntity] = entity2

    ENTITIES[data['name']] = entity

def writeFile(path_template, path_output, entity):
    # Open template
    with open(getPathFileInStatic(path_template)) as f:
        template = Template(f.read())
    data = template.render(entity=entity)

    # Write file into the directory
    with open(path_output, "w") as f:
        f.write(data)

def writeAppFile():
    # Open template
    with open(getPathFileInStatic("template/app.py.j2")) as f:
        template = Template(f.read())
    data = template.render(entities=list(ENTITIES.values()))

    # Write file into the directory
    # with open("src/app.py", "w") as f:

    with open("src/__init__.py", "w") as f:
        f.write(data)
        info("[x] create (or updated) __init__.py")

def generateEntitiesFiles(entity):
    writeFile("template/entity.py.j2", "src/Models/{0}Entity.py".format(entity.nameEntity), entity)
    info("[x] {0}Entity file created".format(entity.nameEntity))

def generateRepositoriesFiles(entity):
    writeFile("template/repository.py.j2", "src/Repositories/{0}Repository.py".format(entity.nameEntity), entity)
    info("[x] {0}Repository file created".format(entity.nameEntity))

def generateDTOsFiles(entity):
    writeFile("template/dtoV1.py.j2", "src/DTOs/{0}DTO.py".format(entity.nameEntity), entity)
    info("[x] {0}DTO file created".format(entity.nameEntity))

def generateMappeursFiles(entity):
    writeFile("template/mappeur.py.j2", "src/Mappeurs/{0}Mappeur.py".format(entity.nameEntity), entity)
    info("[x] {0}Mappeur file created".format(entity.nameEntity))

def generateServicesFiles(entity):
    writeFile("template/service.py.j2", "src/Services/{0}Service.py".format(entity.nameEntity), entity)
    info("[x] {0}Service file created".format(entity.nameEntity))

def generateAssociatedTableFiles(associatedTable):
    writeFile("template/associatedTable.py.j2", "src/Models/{0}.py".format(associatedTable.name), associatedTable)
    info("[x] {0} file created".format(associatedTable.name))

def generateParsersFiles(entity):
    writeFile("template/parser.py.j2", "src/Parsers/{0}Parser.py".format(entity.nameEntity), entity)
    info("[x] {0}Parser file created".format(entity.nameEntity))

def generateRessourcesFiles(entity):
    writeFile("template/ressource.py.j2", "src/Ressources/{0}Ressource.py".format(entity.nameEntity), entity)
    info("[x] {0}Ressource file created".format(entity.nameEntity))

# TESTS
def generateEntitiesTestsFiles(entity):
    writeFile("template/entityTest.py.j2", "Tests/Models/test_{0}EntityTest.py".format(entity.nameEntity), entity)
    info("[x] {0}EntityTest file created".format(entity.nameEntity))

def generateDTOsTestsFiles(entity):
    writeFile("template/dtoV1Test.py.j2", "Tests/DTOs/test_{0}DTOTest.py".format(entity.nameEntity), entity)
    info("[x] {0}DTOTest file created".format(entity.nameEntity))

def generateMappeursTestsFiles(entity):
    writeFile("template/mappeurTest.py.j2", "Tests/Mappeurs/test_{0}MappeurTest.py".format(entity.nameEntity), entity)
    info("[x] {0}MappeurTest file created".format(entity.nameEntity))

def generateRessourcesTestsFiles(entity):
    writeFile("template/ressourceTest.py.j2", "Tests/Ressources/test_{0}RessourceTest.py".format(entity.nameEntity), entity)
    info("[x] {0}RessourceTest file created".format(entity.nameEntity))

def generateRepositoriesTestsFiles(entity):
    writeFile("template/repositoryTest.py.j2", "Tests/Repositories/test_{0}RepositoryTest.py".format(entity.nameEntity), entity)
    info("[x] {0}RepositoryTest file created".format(entity.nameEntity))

def generateServicesTestsFiles(entity):
    writeFile("template/serviceTest.py.j2", "Tests/Services/test_{0}ServiceTest.py".format(entity.nameEntity), entity)
    info("[x] {0}ServiceTest file created".format(entity.nameEntity))

def generateMocksTestsFiles(entity):
    writeFile("template/mock.py.j2", "Tests/Mocks/{0}Mock.py".format(entity.nameEntity), entity)
    info("[x] {0}Mock file created".format(entity.nameEntity))

def generateFiles():
    for name in ENTITIES.keys():
        entity = ENTITIES[name]
        generateEntitiesFiles(entity)
        generateRepositoriesFiles(entity)
        generateDTOsFiles(entity)
        generateMappeursFiles(entity)
        generateServicesFiles(entity)
        generateParsersFiles(entity)
        generateRessourcesFiles(entity)

        # tests
        generateEntitiesTestsFiles(entity)
        generateDTOsTestsFiles(entity)
        generateMappeursTestsFiles(entity)
        # generateRessourcesTestsFiles(entity)
        generateRepositoriesTestsFiles(entity)
        generateServicesTestsFiles(entity)
        generateMocksTestsFiles(entity)

    for associateTable in ASSOCIATETABLES:
        generateAssociatedTableFiles(associateTable)

    writeAppFile()

if __name__ == "__main__":
    cond_stop = False
    choose_step = [inquirer.List('choose', message="What now", choices=['Create entity', 'Stop'])]

    while not cond_stop:
        step_answer = inquirer.prompt(choose_step)

        if step_answer['choose'] == 'Create entity':
            createEntity()
        else:
            cond_stop = True
    init()
    generateFiles()
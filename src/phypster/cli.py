import argparse, json, inquirer
from .phypster import Phypster


import setuptools as _

def main():
    #############
    # argsparse #
    #############
    parser = argparse.ArgumentParser(description='Flask starter')
    parser.add_argument('--import_json', type=str, help='import json model')
    parser.add_argument('-d', '--debug', action='store_true', help="enable debug log during the application generation")

    args = parser.parse_args()
    phypster = Phypster()

    phypster.DEBUG = args.debug

    print("DEBUG = {0}".format(phypster.DEBUG))

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

if __name__ == "__main__":
    main()
import argparse
from .phypster import Phypster

def main():
    #############
    # argsparse #
    #############
    parser = argparse.ArgumentParser(description='Flask starter')
    parser.add_argument('--import_json', help='import json model')

    args = parser.parse_args()

    print(args)

    # phypster = Phypster()

    # if args.import_json != None:
    #     with open("mocks.json", "r") as f:
    #         data_json = json.load(f)

    #     for data_enum in data_json["enums"]:
    #         phypster.createEnum(data_enum)

    #     for data_entity in data_json["entities"]:
    #         phypster.createEntity(data_entity)
    # else:
    #     cond_stop = False
    #     choose_step = [inquirer.List('choose', message="What now", choices=['Create entity', 'Create enum', 'Stop'])]

    #     while not cond_stop:
    #         step_answer = inquirer.prompt(choose_step)

    #         if step_answer['choose'] == 'Create entity':
    #             phypster.createEntity()
    #         elif step_answer['choose'] == 'Create enum':
    #             phypster.createEnum()
    #         else:
    #             cond_stop = True
    # phypster.init()
    # phypster.generateFiles()

if __name__ == "__main__":
    main()
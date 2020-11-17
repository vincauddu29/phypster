# Phypster

Jhypster for python developper. Flask starter.

\#Jhypster \#Python \#Flask

## Install
1) git clone
2) make install

## Build a new application
### JSON file (Recommanded)
1) Write your JSON file
This file describe your entities

Sample:
```
{
    "enums": [
        {
            "name": "MyEnum",
            "listItems": [
                "field1",
                "field2"
            ]
        }
    ],
    "entities": [
        {
            "name": "MyEntity1",
            "columns": [
                ["name", "String", false, false],
                ["col1", "Float", false, false],
                ["col2", "DateTime", false, false]
            ],
            "relationships": [],
            "enums": [
                {
                    "name": "MyEnum",
                    "nullable": true
                }
            ]
        },
        {
            "name": "MyEntity2",
            "columns": [
                ["identity", "Integer", true, true],
                ["name", "String", false, false]
            ],
            "relationships": [
                {
                    "entity2": "MyEntity1",
                    "typeRelation": "One to Many"
                }
            ],
            "enums": []
        }
    ]
}
```

2) Build the application
```
python3 phypster.py --import_json=myApp.json
```
### Cli
1) Run phypster
```
python3 phypster.py
```
2) Create yours enums
3) Create yours entities


## Structure
* Models -> Entity files, entity model connected to the database
* DTOs -> Entity converted to json, send to the client
* Mappeurs -> Convert Entity to DTO and DTO to Entity
* Enums -> Enum files
* Repositories -> Repository files, group database queries
* Services -> Service files, connect ressource to repository
* Ressources -> Ressource files, entrypoints
* Parsers -> Files to define http params
* Config -> Config applications files

CLIENT <- (DTO) -> RESSOURCE <- (DTO) -> SERVICE <- (Entity) -> REPOSITORY <- (Entity) -> DATABASE

## Contributing
Enjoy :) and make pull request.

[ ] Write more tests
[ ] Write documentation
[ ] Implement jdl (jhypster file) parser
[x] Implement installer

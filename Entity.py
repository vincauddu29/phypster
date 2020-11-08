from typing import List


class Column:
    def __init__(self, name: str, typeData: str, primary: bool, nullable: bool = False):
        self.nameColumn: str = name
        self.typeData: str = typeData
        self.primary: bool = primary
        self.nullable: bool = nullable

    def typeDataPython(self):
        if self.typeData == 'Integer':
            return 'int'
        elif self.typeData == 'Float':
            return 'float'
        elif self.typeData == 'Boolean':
            return 'bool'
        elif self.typeData == 'DateTime':
            return 'inputs.datetime_from_iso8601'
        else:
            return 'str'

class RelationShip:
    def __init__(self, entity1, entity2, isOneToOne: bool = False, isOneToMany: bool = False, isManyToOne: bool = False, isManyToMany: bool = False, associateTable = None):
        self.entity1: Entity = entity1
        self.entity2: Entity = entity2
        self.isOneToOne: bool = isOneToOne
        self.isOneToMany: bool = isOneToMany
        self.isManyToOne: bool = isManyToOne
        self.isManyToMany: bool = isManyToMany
        self.associateTable: AssociateTable = associateTable

class AssociateTable:
    def __init__(self, entity1, entity2):
        self.name: str = "tj_" + entity1.nameEntity.lower() + "_" + entity1.subName + "_" + entity2.nameEntity.lower() + "_" + entity2.subName
        self.entity1: Entity = entity1
        self.entity2: Entity = entity2

class EnumEntity:
    def __init__(self, name: str) -> None:
        self.nameEnum: str = name
        self.listItems: List[str] = []

    def addItem(self, item: str):
        self.listItems.append(item)

class EnumColumn:
    def __init__(self, enum: EnumEntity, nullable: bool) -> None:
        self.enum: EnumEntity = enum
        self.nullable: bool = nullable

class Entity:
    def __init__(self, name: str):
        self.nameEntity: str = name
        self.primaryKey: bool = None
        self.subName: str = name[0:3].lower()
        self.columns: List[Column] = []
        self.relationships: List[RelationShip] = []
        self.enums: List[EnumColumn] = []

    def addColumn(self, nameColumn: str, typeData: str, primary: bool = False, nullable: bool = False):
        if primary:
            self.primaryKey = Column(nameColumn, typeData, True)
        else:
            self.columns.append(Column(nameColumn, typeData, False, nullable=nullable))
        
    def addRelationShip(self, relationship: RelationShip):
        self.relationships.append(relationship)

    def addEnum(self, myEnum: EnumEntity, nullable: bool = False):
        self.enums.append(EnumColumn(myEnum, nullable))

    def getPrimaryKey(self):
        if self.primaryKey == None:
            self.primaryKey = Column("id", "Integer", True)
        return self.primaryKey

    def getRandomInt(self) -> int:
        import random
        return random.randint(1, 2000)

    def haveOneToManyOrManyToOne(self) -> bool:
        for r in self.relationships:
            if r.isManyToOne or r.isOneToMany:
                return True
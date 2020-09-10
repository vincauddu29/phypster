class Column:
    def __init__(self, name: str, typeData: str, primary: bool, nullable: bool = False):
        self.nameColumn = name
        self.typeData = typeData
        self.primary = primary
        self.nullable = nullable

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
        self.entity1 = entity1
        self.entity2 = entity2
        self.isOneToOne = isOneToOne
        self.isOneToMany = isOneToMany
        self.isManyToOne = isManyToOne
        self.isManyToMany = isManyToMany
        self.associateTable = associateTable

# class ForeignKey:
#     def __init__(self, foreignKeyColumn, entity, typeData: str, nullable: bool = False):
#         self.entity = entity
#         self.foreignKeyColumn = foreignKeyColumn
#         self.nullable = nullable
#         self.typeData = typeData

class Entity:
    def __init__(self, name: str):
        self.nameEntity = name
        self.primaryKey = None
        self.subName = name[0:3].lower()
        self.columns = []
        self.relationships = []
        # self.foreignkeys = []

    def addColumn(self, nameColumn: str, typeData: str, primary: bool = False, nullable: bool = False):
        if primary:
            self.primaryKey = Column(nameColumn, typeData, True)
        else:
            self.columns.append(Column(nameColumn, typeData, False, nullable=nullable))
        
    def addRelationShip(self, relationship):
        self.relationships.append(relationship)

    # def addForeignKey(self, entity, foreignKeyColumn, typeData: str = "Integer", nullable: bool = False):
    #     self.foreignkeys.append(ForeignKey(foreignKeyColumn, entity, typeData, nullable))

    def getPrimaryKey(self):
        if self.primaryKey == None:
            self.primaryKey = Column("id", "Integer", True)
        return self.primaryKey

class AssociateTable:
    def __init__(self, entity1, entity2):
        self.name = "tj_" + entity1.nameEntity.lower() + "_" + entity1.subName + "_" + entity2.nameEntity.lower() + "_" + entity2.subName
        self.entity1 = entity1
        self.entity2 = entity2

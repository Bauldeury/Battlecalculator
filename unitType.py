import csv
import config

unitTypes:"dict[str,UnitType]" = {}

class UnitType:
    integerValues = {"life","move","attack"}

    def __init__(self):
        self.key:str = None
        self.name:str = None
        self.type:str = None
        self.subtype:str = None
        self.life:int = None
        self.move:int = None
        self.attack:int = None
        self.armor:int = None

def loadUnitTypes():
    with open(config.unitTypesFile) as csvfile:
        reader = csv.reader(csvfile,delimiter=config.delimiter,lineterminator=config.lineTerminator)
        columnsIDs:"dict[str,int]" = {}

        for row,values in enumerate(reader):
            if row == 0:
                blankUnitType = UnitType()
                for valueName in blankUnitType.__dict__:
                    columnsIDs[valueName]= values.index(valueName)
            else:
                unitType = UnitType()
                for valueName in columnsIDs:
                    unitType.__dict__[valueName] = values[columnsIDs[valueName]]
                    if valueName in unitType.integerValues:
                        unitType.__dict__[valueName] = int(unitType.__dict__[valueName])
                #print(unitType.__dict__)
                unitTypes[unitType.key]=unitType

import unitType
import config

units:"dict[str,Unit]" = {}
maxX = 0
maxY = 0
class Unit:
    def __init__(self) -> None:
        self.key:str = None
        self.type:unitType.UnitType = None
        self.count:int = None
        self.faction:"['up']|['down']" = None
        self.position:tuple[int,int] = None
        self.isCharging:bool = False

    def export(self):
        output = list()
        output.append("unit")
        output.append(self.key)
        output.append("faction")
        output.append(self.faction)
        output.append("type")
        output.append(self.type.key)
        output.append("count")
        output.append(self.count)

        return output


    def _directionForward(self):
        if self.faction=="up":
            return (0,-2)
        else:
            return (0,2)

    def _directionForwardLeft(self):
        if self.faction=="up":
            return (-1,-1)
        else:
            return (1,1)

    def _directionForwardRight(self):
        if self.faction=="up":
            return (1,-1)
        else:
            return (-1,1)

    def getUnitForward(self):
        return getUnitOnPos(_tupleSum(self.position,self._directionForward()))
    def getUnitForwardLeft(self):
        return getUnitOnPos(_tupleSum(self.position,self._directionForwardLeft()))
    def getUnitForwardRight(self):
        return getUnitOnPos(_tupleSum(self.position,self._directionForwardRight()))
    def getUnitBackward(self):
        return getUnitOnPos(_tupleSum(self.position,_tupleNeg(self._directionForward())))
    def getUnitBackwardLeft(self):
        return getUnitOnPos(_tupleSum(self.position,_tupleNeg(self._directionForwardLeft())))
    def getUnitBackwardRight(self):
        return getUnitOnPos(_tupleSum(self.position,_tupleNeg(self._directionForwardRight())))

def loadUnit(args:"list[str]"):
    global units

    unit = Unit()

    for label in {"unit","faction","type","count"}:
        if label not in args:
            raise Exception("ERROR: {} not defined in {}".format(label,args))
        if args.index(label) == len(args):
            raise Exception("ERROR: {} not defined in {}".format(label,args))
        
        value = args[args.index(label) +1]

        if label == "unit":
            if value == "":
                raise Exception("ERROR: {} is '{}'. It should be defined".format(label,value))
            if value in units:
                raise Exception("ERROR: {} is already defined".format(value))
            unit.key = value
            units[unit.key]=unit

                
        if label == "faction":
            if value not in {"up","down"}:
                raise Exception("ERROR: {} is '{}'. It should either be 'up' or 'down'".format(label,value))
            unit.faction = value

        if label == "type":
            if value not in unitType.unitTypes:
                raise Exception("ERROR: {} is '{}'. It has not been defined in '{}'".format(label,value,config.unitTypesFile))
            unit.type = unitType.unitTypes[value]

        if label == "count":
            if value.isdigit() == False:
                raise Exception("ERROR: {} is '{}'. It must be a positive integer".format(label,value))
            unit.count = int(value)

    if "is_charging" in args:
        unit.isCharging = True
        print("CHARGGEEEEEE")


    units[unit.key] = unit

def placeUnit(pos:"tuple[int,int]",unitKey:str):
    global units, maxX, maxY

    if unitKey not in units:
        raise Exception("ERROR: '{}' has not been set.".format(unitKey))
    
    unit = units[unitKey]

    if unit.position != None:
        raise Exception("ERROR: '{}' has already a position {}.".format(unitKey,unit.position))

    if pos[0] > maxX: maxX = pos[0]
    if pos[1] > maxY: maxY = pos[1]

    unit.position = pos

def getUnitOnPos(pos:"tuple[int,int]"):
    for unit in units.values():
        if unit.position == pos:
            return unit

    return None

def _tupleSum(t1:"tuple[int,int]",t2:"tuple[int,int]"):
    return (t1[0]+t2[0],t1[1]+t2[1])

def _tupleScale(t:"tuple[int,int]",s:int):
    return (t[0]*s, t[1]*s)

def _tupleNeg(t:"tuple[int,int]"):
    return (-t[0], -t[1])

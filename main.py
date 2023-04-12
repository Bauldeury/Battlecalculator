import csv
import config
import random
import unitType
import unit



def loadScenario():
    with open(config.scenarioFile) as csvfile:
        reader = csv.reader(csvfile,delimiter=config.delimiter)

        nonMapLinesCount = 0
        for row,values in enumerate(reader):
            if values[0] == "unit":
                unit.loadUnit(values)
                nonMapLinesCount +=1
            elif values[0] == "comment":
                nonMapLinesCount +=1
            else:
                for column, value in enumerate(values):
                    if value not in {"","_"," "}:
                        unit.placeUnit((column,row-nonMapLinesCount),value)


def computeScenario():
    for u in unit.units.values():
        u._damageTaken = 0
        u._currentDirection = "FORWARD"
        for neighboor,direction in {
            (u.getUnitForward(),"FORWARD"),(u.getUnitForwardLeft(),"FORWARD"),(u.getUnitForwardRight(),"FORWARD"),
            (u.getUnitBackward(),"BACKWARD"),(u.getUnitBackwardLeft(),"BACKWARD"),(u.getUnitBackwardRight(),"BACKWARD")
            }:
            if neighboor != None:
                u._currentDirection = direction
                break

    for u in unit.units.values():

        frontUnits:"set[unit.Unit]" = set()
        backUnits:"set[unit.Unit]" = set()
        for neighboor in {u.getUnitForward(),u.getUnitForwardLeft(),u.getUnitForwardRight()}:
            if neighboor != None:
                if neighboor.faction != u.faction:
                    frontUnits.add(neighboor)
        for neighboor in {u.getUnitBackward(),u.getUnitBackwardLeft(),u.getUnitBackwardRight()}:
            if neighboor != None:
                if neighboor.faction != u.faction:
                    backUnits.add(neighboor)

        if len(frontUnits) > 0:
            for enemy in frontUnits:
                damage = (u.type.attack * u.count) * (1 + calculateWeaponBonus(u,enemy) + calculateRandomDeviation()) / len(frontUnits)
                enemy._damageTaken += damage
        elif len(backUnits) > 0:
             for enemy in backUnits:
                damage = (u.type.attack * u.count) * (1 + calculateWeaponBonus(u,enemy) + calculateRandomDeviation() + calculateFlankingBonus(u,enemy,enemy._currentDirection)) / len(backUnits)
                enemy._damageTaken += damage


    for u in unit.units.values():
        u.count = int(u.count - u._damageTaken/u.type.life)

def calculateWeaponBonus(attacker:unit.Unit, defender:unit.Unit) -> float:
    '''Output: 0 is neutral, 1 is doubling damage, -0.5 is halving damage'''
    output = 0

    ### NON SPECIFIC BONUSES
    if attacker.type.subtype == "SHIELD" and defender.type.subtype == "HAST":
        output+= .25
    if attacker.type.subtype == "SHIELD" and defender.type.type == "RANGED":
        output+= .25


    ### INFANTRY SPECIFIC BONUSES
    if attacker.type.type == "INFANTRY":
        if attacker.type.subtype == "HAST" and defender.type.subtype == "TWO_HANDED":
            output+= .25
        if attacker.type.subtype == "HAST" and defender.type.type == "CAVALRY":
            output+= .25
        if attacker.type.subtype == "TWO_HANDED" and defender.type.subtype == "TWO_WEAPONS":
            output+= .25
        if attacker.type.subtype == "TWO_HANDED" and defender.type.subtype == "SHIELD":
            output+= .25
        if attacker.type.subtype == "TWO_WEAPONS" and defender.type.subtype == "SHIELD":
            output+= .25
        if attacker.type.subtype == "TWO_WEAPONS" and defender.type.type == "RANGED":
            output+= .25

        
    ### CAVALRY SPECIFIC BONUSES
    if attacker.type.type == "CAVALRY":
        if attacker.type.subtype == "HAST" and attacker.isCharging == True:
            output+= .5
    
    return output

def calculateRandomDeviation() -> float:
    '''Output: 0 is neutral, 1 is doubling damage, -0.5 is halving damage'''
    return (random.random()*2-1)*config.randomPart

def calculateFlankingBonus(attacker:unit.Unit, defender:unit.Unit,defenderOrientation:str) -> float:
    '''Output: 0 is neutral, 1 is doubling damage, -0.5 is halving damage'''
    if defenderOrientation != "FORWARD" :
        return 0
    if defender.getUnitBackward() == attacker :
        return config.backstabBonus
    elif defender.getUnitBackwardLeft() == attacker or defender.getUnitBackwardRight() == attacker:
        return config.flankingBonus
    return 0

def outputResults():
    with open(config.outputFile,"w",newline=config.lineTerminator) as csvfile:
        writer = csv.writer(csvfile,delimiter=config.delimiter,lineterminator=config.lineTerminator)
        for u in unit.units.values():
            #print(u.export())
            writer.writerow(u.export())

        for y in range(0,unit.maxY+1):
            for x in range(0,unit.maxX+1):
                u = unit.getUnitOnPos((x,y))
                if u != None : csvfile.write(u.key)
                csvfile.write(config.delimiter)
            csvfile.write(config.lineTerminator)





def main():
    print("BATTLE CALCULATOR")
    unitType.loadUnitTypes()
    print("UnitTypes loaded...")
    loadScenario()
    print("Scenario loaded...")
    computeScenario()
    print("Scenario computed!")
    outputResults()
    print("Output writen at {}".format(config.outputFile))
    print()



if __name__ == "__main__":
    main()
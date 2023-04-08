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
        u.damageTaken = 0

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
                enemy.damageTaken += damage
        elif len(backUnits) > 0:
             for enemy in backUnits:
                damage = (u.type.attack * u.count) * (1 + calculateWeaponBonus(u,enemy) + calculateRandomDeviation()) / len(backUnits)
                enemy.damageTaken += damage


    for u in unit.units.values():
        u.count = int(u.count - u.damageTaken/u.type.life)

def calculateWeaponBonus(attacker:unit.Unit, defender:unit.Unit):
    '''Output: 0 is neutral, 1 is doubling damage, -0.5 is halving damage'''
    output = 0

    ### NON SPECIFIC BONUSES
    if attacker.type.subtype == "SHIELD" and defender.type.subtype == "HAST":
        output+= .5
    if attacker.type.subtype == "SHIELD" and defender.type.type == "RANGED":
        output+= .25


    ### INFANTRY SPECIFIC BONUSES
    if attacker.type.type == "INFANTRY":
        if attacker.type.subtype == "HAST" and defender.type.subtype == "TWO_HANDED":
            output+= .5
        if attacker.type.subtype == "HAST" and defender.type.type == "CAVALRY":
            output+= .25
        if attacker.type.subtype == "TWO_HANDED" and defender.type.subtype == "TWO_WEAPONS":
            output+= .5
        if attacker.type.subtype == "TWO_HANDED" and defender.type.subtype == "SHIELD":
            output+= .25
        if attacker.type.subtype == "TWO_WEAPONS" and defender.type.subtype == "SHIELD":
            output+= .5
        if attacker.type.subtype == "TWO_WEAPONS" and defender.type.type == "RANGED":
            output+= .25

        
    ### CAVALRY SPECIFIC BONUSES
    if attacker.type.type == "CAVALRY":
        pass #NOTHING

    return output

def calculateRandomDeviation():
    return (random.random()*2-1)*config.randomPart

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
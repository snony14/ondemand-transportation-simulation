print("Hello Momo")
busCapacity = "busCapacity"

inputDict = dict()
inputDict['busCapacity'] = False
inputDict['boardingTime'] = False
inputDict['requestRate'] = False
inputDict['pickupInterval'] = False
inputDict['maxDelay'] = False
inputDict['noBuses'] = False
inputDict['noStops'] = False
inputDict['map'] = False
inputDict['stopTime'] = False


def readFile(fileName):
    wb = open("../data/basic_input.txt", "r")
    # parse input and save it into dictionary
    for line in wb:
        split_line = line.split()
        fst = split_line[0]
        valid = False
        if len(fst) > 1 and fst[0] != '#':
            valid = True
        elif len(fst) == 1 and fst != "#":
            valid = True

        if valid and fst in inputDict:
            inputDict[fst] = split_line[1:]
        elif valid and inputDict['map'] != False and inputDict['stopTime'] == False:
            inputDict['map'].append(split_line)
    wb.close()
    # validate inputs or throw an error
    # try  and catch and then throw
    validateInt('busCapacity', inputDict['busCapacity'], "s")
    validateInt('boardingTime', inputDict['boardingTime'], "s")
    validateFloat('requestRate', inputDict['requestRate'])
    validateFloat('pickupInterval', inputDict['pickupInterval'])
    validateInt('maxDelay', inputDict['maxDelay'], "s")
    validateInt('noBuses', inputDict['noBuses'], "s")
    validateInt('noStops', inputDict['noStops'], "s")
    # validate map
    validateInt('stopTime', inputDict['stopTime'], "s")

    return inputDict


def validateInt(name, content=[], check='b'):
    # positive, or negative number, or both
    isAllValid = True
    # for v in content:
    for v in content:
        if check == 'b':
            if not isNumber(v, 'b'):
                print("Value %s is not an integer for variable %s" % (v, name))
                break
        else:
            if not isNumber(v, 's'):
                print("Value %s is not a positive integer for variable %s" % (v, name))
                break

    return isAllValid


def validateFloat(name, content=[]):
    isAllValid = True
    for v in content:
        if not isFloat(v):
            print("Value %s is not a float for variable %s" % (v, name))
            break
    return isAllValid


def isFloat(value: str = "") -> bool:
    isValid = True
    points = 0
    for c in value:
        if not c.isdigit() and c == '.':
            points += 1
        elif not c.isdigit():
            isValid = False
    if points != 1:
        isValid = False
    return isValid


def isNumber(value, checks):
    isValid = True
    isDigit = (value[0] == '-'
               ) if checks == "b" else value[0].isdigit()
    if isDigit:
        for c in value[1:]:
            if not c.isdigit():
                isValid = False
                break
        return isValid
    else:
        return False

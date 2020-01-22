from input import readFile
from request import getNextTimeToGenerateReq, getPickupTime

# parse the inputs, catch the errors

inputDict = readFile('../data/basic_input')
# print(inputDict)

stopTime = int(inputDict['stopTime'][0])*3600
counter = 0
totalReq = 0
while counter <= stopTime:
    print(counter)
    counter += getNextTimeToGenerateReq(
        round(float(inputDict['requestRate'][0]), 2))*3600
    totalReq += 1

print("Total generated request %d" % totalReq)

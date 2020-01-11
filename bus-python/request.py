from random import randint, seed, random
import time
import math


def generateRandom(low=1, high=5):
    return randint(low, high)


'''
Be careful with the time, is it in seconds or min etc...
'''


def getPickupTime(pickupInterval=30):
    seed(int(time.time()))
    rand_value = random()
    while rand_value == 0:
        seed(int(time.time()))
        rand_value = random()
    desiredPickUpTime = (-1)*pickupInterval*math.log(rand_value)
    return desiredPickUpTime


def getNextTimeToGenerateReq(mean=30):
    seed(int(time.time()))
    rand_value = random()
    while rand_value == 0:
        seed(int(time.time()))
        rand_value = random()
    rate = 1 / mean
    nextTimeToGenerateReq = -(math.log(rand_value))*rate
    return nextTimeToGenerateReq


class Request:

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.desiredPickupTime = 0
        self.shortestPathTime = 0

    def setDesiredPickupTime(self, newPickupTime):
        self.desiredPickupTime = newPickupTime

    def setShortestPathTime(self, shortestPathTime):
        self.shortestPathTime = shortestPathTime

from random import randint, seed, random
import time
import math
from output import get_formatted_time


def generate_random(low=1, high=5):
    return randint(low, high)


'''
Be careful with the time, is it in seconds or min etc...
'''


def get_pickup_time(pickup_interval=30):
    seed(int(time.time()))
    rand_value = random()
    while rand_value == 0:
        seed(int(time.time()))
        rand_value = random()
    return (-1)*pickup_interval*math.log(rand_value)


def get_next_time_to_generate_req(mean=30):
    seed(int(time.time()))
    rand_value = random()
    while rand_value == 0:
        seed(int(time.time()))
        rand_value = random()
    rate = 1 / mean
    return -(math.log(rand_value))*rate


class Request:

    def __init__(self, src: int, dst: int, desired_pickup_time: int):
        self.src = src
        self.dst = dst
        self.scheduled_pickup_time = desired_pickup_time
        self.desired_pickup_time = desired_pickup_time
        self.is_truly_scheduled = False

    def set_scheduled_pickup_time(self, new_pickup_time):
        self.scheduled_pickup_time = new_pickup_time

    def set_is_truly_scheduled(self, done: bool):
        self.is_truly_scheduled = done

    def __str__(self):
        return "(%s-%s) time: %s" % (self.src, self.dst, get_formatted_time(self.scheduled_pickup_time))

    def __repr__(self):
        return repr(self.__str__())

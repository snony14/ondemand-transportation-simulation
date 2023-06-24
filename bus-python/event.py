from enum import Enum
from request import Request
from typing import List
from output import get_formatted_time


class EventEnum(Enum):
    NEW_REQUEST = 1
    BOARDING = 2
    DISEMBARK = 3
    BUS_ARRIVE = 4
    BUS_LEAVE = 5
    WAIT = 6
    NOOP = 7


class Event:

    def __init__(self, event_type: EventEnum, event_time: int):
        self.event_type = event_type
        self.event_time = event_time

    def __str__(self):
        return "Event: %s, time: %s" % (self.event_type, get_formatted_time(self.event_time))

    def __repr__(self):
        return repr(self.__str__())


class EventAction:
    def __init__(self, event_type: EventEnum, time: int):
        self.event = Event(event_type, time)
        self.current_station: int = 0
        self.on_board: List[Request] = []
        self.disembark = None

    def set_current_station(self, current_station: int):
        self.current_station = current_station

    def set_board(self, req: Request):
        self.on_board.append(req)

    def set_disembark(self, req: Request):
        self.on_board[:] = (old_req for old_req in self.on_board if
                            old_req.scheduled_pickup_time != req.scheduled_pickup_time)
        self.disembark = req

    def get_event_type(self):
        return self.event.event_type

    def get_event_time(self):
        return self.event.event_time

    def set_event_time(self, t: int):
        self.event.event_time = t

    def __str__(self):
        return "%s station %s" % (self.event.__repr__(),  self.current_station)

    def __repr__(self):
        return repr(self.__str__())




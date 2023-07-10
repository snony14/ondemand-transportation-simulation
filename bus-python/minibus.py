from event import EventAction, EventEnum
from request import Request
from typing import List
from route_planner import generate_event_actions, get_journey_data
import math

class Minibus:

    def __init__(self, capacity: int, index: int):
        self.maxBusCapacity = 24
        self.capacity = capacity
        self.id = index
        self.scheduled_request: List[Request] = []
        # subject to adjust time if a bus is to leave
        self.journey: List[EventAction] = [EventAction(EventEnum.WAIT, 9999999)]
        self.potential_journey: List[EventAction] = []

    def update_initial_event_time(self, t: int):
        init_event_action = self.journey[0]
        init_event_action.set_event_time(t)
        self.journey = [init_event_action]

    def add_to_scheduled(self, request):
        self.scheduled_request.append(request)

    def execute_event(self):
        fst = self.journey[0]
        # HANDLE THIS WITH A WAIT
        if len(self.potential_journey) > 0:
            self.journey = [self.potential_journey[0]]
            self.potential_journey = self.potential_journey[1:]
        else:
            self.journey = [EventAction(EventEnum.WAIT, 9999999)]
        if fst.get_event_type() == EventEnum.BOARDING:
            ids = [req.id for req in fst.on_board]
            scheduled_request = [req for req in self.scheduled_request if req.id not in ids]
            self.scheduled_request = scheduled_request
        return fst

    def set_potential_journey(self, new_journey: List[EventAction]):
        self.potential_journey = new_journey

    def board_first_heuristic(self, req: Request, time: int):
        scheduled_request = [r for r in self.scheduled_request]
        scheduled_request.append(req)
        scheduled_request = sorted(scheduled_request, key=lambda r: r.scheduled_pickup_time)
        if self.journey[0].get_event_type() == EventEnum.WAIT:
            self.journey[0].set_event_time(time)
        journey: List[EventAction] = [self.journey[0]]
        pos = 0
        done = False
        while pos < len(scheduled_request) and done is not True:
            r = scheduled_request[pos]
            new_journey = generate_event_actions(journey[-1], EventEnum.BOARDING, r)
            if new_journey[-1].get_event_type() == EventEnum.NOOP:
                done = True
            else:
                pos += 1
            journey += new_journey[1:]
        board = [req for req in journey[-1].on_board]
        # Disembark paths
        while len(board) > 0:
            r = board[0]
            new_journey = generate_event_actions(journey[-1], EventEnum.DISEMBARK, r)
            journey += new_journey[1:]
            board = [req for req in journey[-1].on_board]
        return journey

    def disembark_heuristic(self, request: Request, time: int):
        board = [req for req in self.journey[0].on_board]
        scheduled_request = [r for r in self.scheduled_request]
        scheduled_request.append(request)
        # this function can be extracted
        scheduled_request = sorted(scheduled_request, key=lambda r: r.scheduled_pickup_time)
        if self.journey[0].get_event_type() == EventEnum.WAIT:
            self.journey[0].set_event_time(time)
        journey: List[EventAction] = [self.journey[0]]
        pos = 0
        done = False
        while pos < len(scheduled_request) and done is not True:
            r = scheduled_request[pos]
            min_time = 900000
            disembark_journey: List[EventAction] = []
            # find on board user which does not violate our requirements: closest to desired pick up time.
            for req in board:
                disembark_journey = generate_event_actions(journey[-1], EventEnum.DISEMBARK, req)
                disembark_journey += generate_event_actions(disembark_journey[-1], EventEnum.BOARDING, r)
                if disembark_journey[-1].get_event_type() != EventEnum.NOOP:
                    if disembark_journey[-1].get_event_time() < min_time:
                        min_time = disembark_journey[-1].get_event_time()
            if len(disembark_journey) > 0 and min_time < 900000:
                journey += [j for j in disembark_journey][1:]
                board = [r for r in journey[-1].on_board]
            else:
                new_journey = generate_event_actions(journey[-1], EventEnum.BOARDING, r)
                if new_journey[-1].get_event_type() == EventEnum.NOOP:
                    done = True
                else:
                    pos += 1
                journey += new_journey[1:]
        board = [req for req in journey[-1].on_board]
        # Disembark paths
        while len(board) > 0:
            r = board[0]
            new_journey = generate_event_actions(journey[-1], EventEnum.DISEMBARK, r)
            journey += new_journey[1:]
            board = [req for req in journey[-1].on_board]

        return journey

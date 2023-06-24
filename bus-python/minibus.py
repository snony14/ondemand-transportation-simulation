from event import EventAction, EventEnum
from request import Request
from typing import List
from route_planner import generate_event_actions


class Minibus:

    def __init__(self, capacity: int):
        self.maxBusCapacity = 24
        self.capacity = capacity
        self.scheduled_request: List[Request] = []
        # subject to adjust time if a bus is to leave
        self.journey: List[EventAction] = [EventAction(EventEnum.WAIT, 0)]

    def update_initial_event_time(self, t: int):
        initial_event = self.journey[0]
        initial_event.set_event_time(t)
        self.journey = [initial_event]

    def board_first_heuristic(self, req: Request):
        scheduled_request = [r for r in self.scheduled_request]
        scheduled_request.append(req)
        scheduled_request = sorted(scheduled_request, key=lambda r: r.scheduled_pickup_time)
        journey: List[EventAction] = [self.journey[-1]]
        pos = 0
        done = False
        has_noop = False
        while pos < len(scheduled_request) and done is not True:
            r = scheduled_request[pos]
            new_journey = generate_event_actions(journey[-1], EventEnum.BOARDING, r)
            if new_journey[-1].get_event_type() == EventEnum.NOOP:
                has_noop = True
                done = True
            else:
                journey += new_journey[1:]
                pos += 1
        return journey

    def disembark_first_heuristic(self):
        pass


bus = Minibus(12)
r1 = Request(5, 2, 600)
r1.set_is_truly_scheduled(True)
r2 = Request(3, 1, 900)
r2.set_is_truly_scheduled(True)
bus.scheduled_request = [r1, r2]

r3 = Request(1, 5, 1200)
print(bus.board_first_heuristic(r3))


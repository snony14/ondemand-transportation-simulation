from minibus import Minibus
from event import RequestEvent
from typing import List
from request import Request
from route_planner import get_journey_data
from event import EventEnum, EventAction
from output import get_formatted_time


def run():
    t = 0
    request_event = RequestEvent()
    minibuses: List[Minibus] = [Minibus(24, i + 1) for i in range(10)]
    req_id = 0
    unsatisfied_reqs = 0
    while t <= 60 * 60:  # 24 * 60 * 60:
        req_time = request_event.get_event_time()
        minibuses.sort(key=lambda b: b.journey[0].get_event_time())
        bus_event_time = minibuses[0].journey[0].get_event_time()
        if req_time <= bus_event_time:
            t = req_time
            new_req = request_event.get_request(t)
            new_req.set_id(req_id)
            # schedule the req and update the time accordingly for all the minibuses
            minibus, journey = generate_journey(minibuses, new_req, t)
            if minibus is not None:
                new_req.set_is_truly_scheduled(True)
                minibus.add_to_scheduled(new_req)
                minibus.set_potential_journey(journey[1:])
                req_id += 1
                if new_req.scheduled_pickup_time < 10*60:
                    print(get_formatted_time(req_time), "-> satisfied by minibus: ", minibus.id, new_req)
            else:
                unsatisfied_reqs += 1
                # print(get_formatted_time(req_time), "-> not satisfied", new_req)
            request_event.generate_next_event(t)
        else:
            action = minibuses[0].execute_event()
            t = action.get_event_time()
            event_type = action.get_event_type()
            if event_type == EventEnum.BUS_ARRIVE or event_type == EventEnum.BUS_LEAVE or event_type == EventEnum.BOARDING or event_type == EventEnum.DISEMBARK:
                output_event(minibuses[0].id, action, t)
    return req_id, unsatisfied_reqs


def generate_journey(minibuses: List[Minibus], req: Request, time: int):
    waiting_time = 0
    minibus = None
    new_journey: List[EventAction] = []
    for bus in minibuses:
        journey = bus.board_first_heuristic(req, time)
        fst, snd, trd = get_journey_data(journey)
        if trd > waiting_time and journey[-1].get_event_type() != EventEnum.NOOP:
            minibus = bus
            new_journey = journey
            waiting_time = trd

    return minibus, new_journey


def output_event(bus_id: int, event: EventAction, time: int):
    event_type = event.get_event_type()
    if event_type == EventEnum.BUS_ARRIVE:
        print("%s -> Bus %s arrives at station %s" % (get_formatted_time(time), bus_id, event.current_station))
    elif event_type == EventEnum.BUS_LEAVE:
        print("%s -> Bus %s leaves station %s" % (get_formatted_time(time), bus_id, event.current_station))
    elif event_type == EventEnum.BOARDING:
        print("%s -> Bus %s boarded a passenger at station %s" % (get_formatted_time(time), bus_id, event.current_station))
        print("%s -> Bus %s occupancy became %s" % (get_formatted_time(time), bus_id, len(event.on_board)))
    elif event_type == EventEnum.DISEMBARK:
        print("%s -> Bus %s disembark a passenger at station %s" % (get_formatted_time(time), bus_id, event.current_station))
        print("%s -> Bus %s occupancy became %s" % (get_formatted_time(time), bus_id, len(event.on_board)))
    else:
        print("Unknown event %s", str(event))


# run()

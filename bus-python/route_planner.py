from event import EventAction, Event, EventEnum
from request import Request
from typing import List
import math

test_network = [[0, 3, -1, -1, -1, 4], [3, 0, 5, -1, -1, -1], [-1, -1, 0, 2, -1, -1], [-1, -1, -1, 0, 2, 2],
                [-1, 1, -1, -1, 0, -1], [4, -1, -1, 2, 4, 0]]

test_boarding_time = 10


def floyd_warshall(network: List[List[int]]):
    total_wedge = len(network)
    dist = [[math.inf for j in range(total_wedge)] for i in range(total_wedge)]
    prev = [[0 for j in range(total_wedge)] for i in range(total_wedge)]
    for i in range(total_wedge):
        for j in range(total_wedge):
            dist[i][j] = network[i][j] * 60 if network[i][j] != -1 else math.inf
            prev[i][j] = i
    for i in range(total_wedge):
        dist[i][i] = 0
        prev[i][i] = i

    for k in range(total_wedge):
        for i in range(total_wedge):
            for j in range(total_wedge):
                new_wedge = dist[i][k] + dist[k][j]
                if dist[i][j] > new_wedge:
                    dist[i][j] = new_wedge
                    prev[i][j] = prev[k][j]
    return dist, prev


def get_path(prev: List[List[int]], i: int, j: int):
    if prev[i][j] is None:
        return []
    path = [j]
    while i != j:
        j = prev[i][j]
        path.append(j)
    path.reverse()
    return path


distance, previous = floyd_warshall(test_network)


def get_path2(i: int, j: int):
    if previous[i][j] is None:
        return []
    path = [j]
    while i != j:
        j = previous[i][j]
        path.append(j)
    path.reverse()
    return path


def get_total_distance(path: List[int]):
    start = 0
    dist = 0
    for i in range(1, len(path)):
        dist += distance[start][i]
        start = i
    return dist


def generate_event_actions(start_event: EventAction, goal: EventEnum, req: Request):
    src = start_event.current_station
    dst = req.src if goal == EventEnum.BOARDING else req.dst
    # generate path from source to destination
    paths = get_path(previous, src, dst)
    pos = 1
    event_lst: List[EventAction] = [start_event]
    current_event = event_lst[0]
    done = False
    while not done:
        event_type = current_event.get_event_type()
        on_board = current_event.on_board
        disembark = get_longest_on_board_passenger(on_board, current_event.current_station)
        if event_type == EventEnum.BUS_ARRIVE:
            if len(disembark) > 0:
                current_event = generate_disembark_event(current_event, disembark)
                event_lst.append(current_event)
                if req == disembark[0]:
                    done = True
            elif req.src == current_event.current_station:
                current_event = generate_boarding_event(current_event, req)
                event_lst.append(current_event)
                if current_event.get_event_type() == EventEnum.BOARDING:
                    done = True
            else:
                current_event = generate_leave_event(current_event)
                event_lst.append(current_event)

        elif event_type == EventEnum.DISEMBARK:
            if len(disembark) > 0:
                current_event = generate_disembark_event(current_event, disembark)
                event_lst.append(current_event)
                if req == disembark[0]:
                    done = True
            elif req.src == current_event.current_station:
                current_event = generate_boarding_event(current_event, req)
                event_lst.append(current_event)
                if current_event.get_event_type() == EventEnum.BOARDING:
                    done = True
            else:
                current_event = generate_leave_event(current_event)
                event_lst.append(current_event)
        elif event_type == EventEnum.BOARDING:
            if dst == current_event.current_station:
                current_event = generate_boarding_event(current_event, req)
                event_lst.append(current_event)
                if current_event.get_event_type() == EventEnum.BOARDING:
                    done = True
            else:
                current_event = generate_leave_event(current_event)
                event_lst.append(current_event)
        elif event_type == EventEnum.BUS_LEAVE:
            if pos < len(paths):
                current_event = generate_arrive_event(pos, current_event, paths)
                event_lst.append(current_event)
                pos += 1
            else:
                done = True
        elif event_type == EventEnum.WAIT:
            current_event = generate_leave_event(current_event)
            event_lst.append(current_event)
        else:
            done = True

    return event_lst


def generate_arrive_event(pos: int, current_event: EventAction, paths: List[int]):
    current_station = current_event.current_station
    next_station = paths[pos]
    next_time = distance[current_station][next_station] + current_event.event.event_time
    new_event_action = EventAction(EventEnum.BUS_ARRIVE, next_time)
    new_event_action.set_current_station(next_station)
    new_event_action.on_board = [r for r in current_event.on_board]
    return new_event_action


def generate_leave_event(current_event: EventAction):
    new_event_action = EventAction(EventEnum.BUS_LEAVE, current_event.event.event_time)
    new_event_action.set_current_station(current_event.current_station)
    new_event_action.on_board = [r for r in current_event.on_board]
    return new_event_action


def generate_disembark_event(current_event: EventAction, disembark: List[Request]):
    new_event_action = EventAction(EventEnum.DISEMBARK, current_event.event.event_time + test_boarding_time)
    new_event_action.set_current_station(current_event.current_station)
    new_event_action.on_board = [r for r in current_event.on_board]
    new_event_action.set_disembark(disembark[0])
    return new_event_action


def generate_boarding_event(current_event: EventAction, req: Request):
    new_event_action = None
    event_time = current_event.get_event_time()
    # print(event_time <= req.scheduled_pickup_time, current_event, req)
    if event_time <= req.scheduled_pickup_time:
        new_time = req.scheduled_pickup_time if event_time < req.scheduled_pickup_time else req.desired_pickup_time + test_boarding_time
        new_event_action = EventAction(EventEnum.BOARDING, new_time)
        new_event_action.on_board = [r for r in current_event.on_board]
        new_event_action.set_board(req)
        new_event_action.set_current_station(current_event.current_station)
    else:
        new_event_action = EventAction(EventEnum.NOOP, event_time)
    return new_event_action


def get_longest_on_board_passenger(on_board: List[Request], station: int):
    reqs = [req for req in on_board if req.dst == station]
    return sorted(reqs, key=lambda req: req.scheduled_pickup_time)


def get_journey_data(journeys: List[EventAction]):
    board = 0
    disembark = 0
    for journey in journeys:
        if journey.get_event_type() == EventEnum.BOARDING:
            board += 1

        if journey.get_event_type() == EventEnum.DISEMBARK:
            disembark += 1
    waiting_time = 0
    initial_journey = journeys[0]
    for journey in journeys[1:]:
        if journey.get_event_type() == EventEnum.BOARDING:
            waiting_time += journey.get_event_time() - initial_journey.get_event_time()
        initial_journey = journey
    return board, disembark, waiting_time
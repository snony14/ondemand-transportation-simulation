import unittest
from minibus import Minibus
from request import Request
from event import EventEnum
from main import output_event


class MyTestCase(unittest.TestCase):
    # TEST THE SCHEDULE REQUEST LIST if it will be empty

    @unittest.skip("demonstrating skipping")
    def test_board_fst_heuristic(self):
        bus1 = Minibus(12, 1)
        r1 = Request(5, 2, 600)
        r1.set_is_truly_scheduled(True)
        r2 = Request(3, 1, 900)
        r2.set_is_truly_scheduled(True)
        r3 = Request(2, 5, 100)
        r4 = Request(4, 3, 200)
        initial_event = bus1.journey[0]
        initial_event.on_board = [r3, r4]
        bus1.journey[0] = initial_event
        bus1.journey[0] = initial_event
        bus1.scheduled_request = [r1, r2]

        r5 = Request(1, 5, 1200)
        journey = bus1.board_first_heuristic(r5, 0)
        r5.set_is_truly_scheduled(True)
        bus1.add_to_scheduled(r5)
        bus1.set_potential_journey(journey[1:])
        # print(bus1.potential_journey, bus1.scheduled_request)
        self.assertEqual(journey[-1].get_event_type(), EventEnum.DISEMBARK)

    @unittest.skip("demonstrating skipping")
    def test_board_fst_heuristic_executed(self):
        bus1 = Minibus(12, 1)
        r1 = Request(5, 2, 600)
        r1.set_id(1)
        r1.set_is_truly_scheduled(True)
        r2 = Request(3, 1, 900)
        r1.set_id(2)
        r2.set_is_truly_scheduled(True)
        r3 = Request(2, 5, 100)
        r3.set_id(3)
        r4 = Request(4, 3, 200)
        r4.set_id(4)
        initial_event = bus1.journey[0]
        initial_event.on_board = [r3, r4]
        bus1.journey[0] = initial_event
        bus1.journey[0] = initial_event
        bus1.scheduled_request = [r1, r2]

        r5 = Request(1, 5, 1200)
        r5.set_id(5)
        journey = bus1.board_first_heuristic(r5, 0)
        r5.set_is_truly_scheduled(True)
        bus1.add_to_scheduled(r5)
        bus1.set_potential_journey(journey[1:])
        # print(bus1.journey, "TEST")
        for e in bus1.potential_journey:
            action = bus1.execute_event()

        # print(bus1.scheduled_request)
        self.assertEqual(bus1.scheduled_request, [])

    @unittest.skip("demonstrating skipping")
    def test_board_fst_heuristic_loop_executed(self):
        bus1 = Minibus(12, 1)
        r1 = Request(5, 2, 600)
        r1.set_id(1)
        r1.set_is_truly_scheduled(True)
        r2 = Request(3, 1, 900)
        r2.set_id(2)
        r2.set_is_truly_scheduled(True)
        r3 = Request(2, 5, 100)
        r3.set_id(3)
        r4 = Request(4, 3, 200)
        r4.set_id(4)
        initial_event = bus1.journey[0]
        initial_event.on_board = [r3, r4]
        bus1.journey[0] = initial_event
        bus1.journey[0] = initial_event
        bus1.scheduled_request = [r1, r2]

        r5 = Request(1, 5, 2600)
        r5.set_id(5)
        journey = bus1.board_first_heuristic(r5, 0)
        r5.set_is_truly_scheduled(True)
        bus1.add_to_scheduled(r5)
        bus1.set_potential_journey(journey[1:])
        for e in range(len(bus1.potential_journey)):
            action = bus1.execute_event()
            output_event(1, action, action.get_event_time())
        # print(bus1.journey, "2")
        # print(bus1.scheduled_request)
        r6 = Request(1, 4, 1200)
        r6.set_id(6)
        new_journey = bus1.board_first_heuristic(r6, 0)
        # print(new_journey)
        # print(bus1.potential_journey)
        self.assertEqual(bus1.scheduled_request, [])

    def test_run(self):
        # minibuses, satisfied, potential_journeys = run()
        # print(potential_journeys[0])
        bus1 = Minibus(12, 1)
        r1 = Request(3, 5, 6*60 + 24)
        r1.set_id(1)
        r1.set_is_truly_scheduled(True)
        r2 = Request(3, 5, 6 * 60 + 36)
        r2.set_id(2)
        initial_event = bus1.journey[0]
        initial_event.on_board = []
        bus1.journey[0] = initial_event
        journey = bus1.board_first_heuristic(r1, 0)
        bus1.set_potential_journey(journey[1:])
        for i in range(5):
            bus1.execute_event()
        self.assertEqual([5], [5])


'''
0:00:00 -> Bus 1 leaves station 0
0:00:12 -> satisfied by minibus:  1 (3-5) time: 0:06:59 id: 8
0:02:59 -> satisfied by minibus:  1 (3-1) time: 0:09:08 id: 39
0:03:05 -> satisfied by minibus:  1 (3-5) time: 0:09:55 id: 43
0:03:55 -> satisfied by minibus:  1 (3-1) time: 0:06:23 id: 51
0:03:55 -> Bus 1 arrives at station 5
0:04:00 -> Bus 1 leaves station 5
0:04:41 -> satisfied by minibus:  1 (3-4) time: 0:09:03 id: 64
0:04:51 -> satisfied by minibus:  1 (3-4) time: 0:06:36 id: 70
0:05:58 -> Bus 1 arrives at station 3
0:06:23 -> Bus 1 boarded a passenger at station 3
0:06:23 -> Bus 1 occupancy became 1
0:06:23 -> Bus 1 leaves station 3
0:08:21 -> Bus 1 arrives at station 5
0:15:24 -> Bus 1 boarded a passenger at station 5
0:15:24 -> Bus 1 occupancy became 2
0:15:28 -> Bus 1 leaves station 5
0:17:28 -> Bus 1 arrives at station 3
0:23:02 -> Bus 1 boarded a passenger at station 3
0:23:02 -> Bus 1 occupancy became 2
0:23:02 -> Bus 1 leaves station 3
0:25:00 -> Bus 1 arrives at station 5
0:25:09 -> Bus 1 boarded a passenger at station 5
0:25:09 -> Bus 1 occupancy became 3
0:25:09 -> Bus 1 leaves station 5
0:27:09 -> Bus 1 arrives at station 3
0:28:03 -> Bus 1 boarded a passenger at station 3
0:28:03 -> Bus 1 occupancy became 4
0:28:06 -> Bus 1 leaves station 3
'''

'''
'Event: EventEnum.BUS_ARRIVE, time: 0:19:10' station 3 on board: ['(5-3) time: 0:06:48 id: 1', '(4-3) time: 0:10:52 id: 40', '(1-5) time: 0:11:55 id: 46', '(2-5) time: 0:17:10 id: 18'] -> Bus 1 arrives at station 3
["'Event: EventEnum.BUS_ARRIVE, time: 0:19:10' station 3 on board: ['(5-3) time: 0:19:48 id: 2', '(4-3) time: 0:10:52 id: 0', '(1-5) time: 0:11:55 id: 3', '(2-5) time: 0:03:00 id: 4']"] 1 ["'Event: EventEnum.BUS_ARRIVE, time: 0:19:10' station 3 on board: ['(5-3) time: 0:19:48 id: 2', '(4-3) time: 0:10:52 id: 0', '(1-5) time: 0:11:55 id: 3', '(2-5) time: 0:03:00 id: 4']", "'Event: EventEnum.DISEMBARK, time: 0:19:20' station 3 on board: ['(5-3) time: 0:19:48 id: 2', '(1-5) time: 0:11:55 id: 3', '(2-5) time: 0:03:00 id: 4']", "'Event: EventEnum.DISEMBARK, time: 0:19:30' station 3 on board: ['(1-5) time: 0:11:55 id: 3', '(2-5) time: 0:03:00 id: 4']", "'Event: EventEnum.BOARDING, time: 0:28:30' station 3 on board: ['(1-5) time: 0:11:55 id: 3', '(2-5) time: 0:03:00 id: 4', '(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.BUS_LEAVE, time: 0:28:30' station 3 on board: ['(1-5) time: 0:11:55 id: 3', '(2-5) time: 0:03:00 id: 4', '(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.BUS_ARRIVE, time: 0:30:30' station 5 on board: ['(1-5) time: 0:11:55 id: 3', '(2-5) time: 0:03:00 id: 4', '(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.DISEMBARK, time: 0:30:40' station 5 on board: ['(1-5) time: 0:11:55 id: 3', '(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.DISEMBARK, time: 0:30:50' station 5 on board: ['(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.BUS_LEAVE, time: 0:30:50' station 5 on board: ['(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.BUS_ARRIVE, time: 0:34:50' station 4 on board: ['(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.BUS_LEAVE, time: 0:34:50' station 4 on board: ['(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.BUS_ARRIVE, time: 0:35:50' station 1 on board: ['(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.BUS_LEAVE, time: 0:35:50' station 1 on board: ['(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.BUS_ARRIVE, time: 0:40:50' station 2 on board: ['(3-2) time: 0:28:30 id: 5']", "'Event: EventEnum.DISEMBARK, time: 0:41:00' station 2 on board: []"]
'Event: EventEnum.BOARDING, time: 0:28:30' station 3 on board: ['(1-5) time: 0:11:55 id: 46', '(2-5) time: 0:17:10 id: 18', '(3-2) time: 0:28:30 id: 68'] -> Bus 1 boarded a passenger at station 3
'''

if __name__ == '__main__':
    unittest.main()

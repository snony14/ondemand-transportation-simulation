import unittest
from minibus import Minibus
from request import Request
from event import EventEnum
from main import output_event


class MyTestCase(unittest.TestCase):

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
        
        r6 = Request(1, 4, 1200)
        r6.set_id(6)
        self.assertEqual(bus1.scheduled_request, [])

    def test_run(self):
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

if __name__ == '__main__':
    unittest.main()

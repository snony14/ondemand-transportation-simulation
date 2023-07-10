import unittest
from route_planner import generate_event_actions
from request import Request
from event import EventAction, EventEnum


class MyTestCase(unittest.TestCase):
    def test_from_leave_event_to_disembark(self):
        on_board = [Request(2, 5, 10*60), Request(3, 5, 6*60)]
        event_action = EventAction(EventEnum.BUS_LEAVE, 0)
        event_action.set_current_station(0)
        event_action.set_board(on_board[0])
        journey = generate_event_actions(event_action, EventEnum.DISEMBARK, on_board[0])
        self.assertEqual(journey[-1].get_event_type(), EventEnum.DISEMBARK)

    def test_from_leave_event_to_board(self):
        on_board = [Request(2, 5, 10*60), Request(3, 5, 6*60)]
        event_action = EventAction(EventEnum.BUS_LEAVE, 0)
        event_action.set_current_station(0)
        journey = generate_event_actions(event_action, EventEnum.BOARDING, on_board[0])
        self.assertEqual(journey[-1].get_event_type(), EventEnum.BOARDING)

    def test_from_board_event_to_board(self):
        on_board = [Request(2, 5, 2*60), Request(3, 5, 15*60)]
        event_action = EventAction(EventEnum.BOARDING, 2*60)
        event_action.set_current_station(0)
        event_action.set_board(on_board[0])
        journey = generate_event_actions(event_action, EventEnum.BOARDING, on_board[1])
        self.assertEqual(journey[-1].get_event_type(), EventEnum.BOARDING)

    def test_from_board_event_to_disembark(self):
        on_board = [Request(2, 5, 2*60), Request(3, 5, 15*60)]
        event_action = EventAction(EventEnum.BOARDING, 2*60+10)
        event_action.set_current_station(2)
        event_action.set_board(on_board[0])
        journey = generate_event_actions(event_action, EventEnum.DISEMBARK, on_board[0])
        self.assertEqual(journey[-1].get_event_type(), EventEnum.DISEMBARK)


if __name__ == '__main__':
    unittest.main()

import unittest
from app.state import State
from app.breadth_first_search import BreadthFirstSearch
import numpy as np

class TestBFSMethods(unittest.TestCase):
    
    def test_generate_new_states_2_pieces(self):
        qtd_blocks = 2

        initial_state = State.get_state_from_value(qtd_blocks, '-WBBW')
        final_states = State.generate_final_states(qtd_blocks)

        bfs = BreadthFirstSearch(qtd_blocks, initial_state, final_states, True)

        n = initial_state

        states = bfs._BreadthFirstSearch__generate_next_state(n)
        map_value = list(map(lambda state: state.value, states))

        self.assertEqual(len(map_value), 2)
        self.assertIn('W-BBW', map_value)
        self.assertIn('BW-BW', map_value)

    def test_open_queue_first_iteration_2_pieces(self):
        qtd_blocks = 2

        initial_state = State.get_state_from_value(qtd_blocks, '-WBBW')
        final_states = State.generate_final_states(qtd_blocks)

        bfs = BreadthFirstSearch(qtd_blocks, initial_state, final_states, True)

        open_queue = []

        s = initial_state
        open_queue.append(s)

        n = s
        next_states = bfs._BreadthFirstSearch__generate_next_state(n)
        open_queue = open_queue + next_states

        open_queue_map_value = list(map(lambda state: state.value, open_queue))

        self.assertEqual(len(open_queue_map_value), 3)
        self.assertIn('-WBBW', open_queue_map_value)
        self.assertIn('W-BBW', open_queue_map_value)
        self.assertIn('BW-BW', open_queue_map_value)
    
    def test_open_queue_first_iteration_2_pieces2(self):
        qtd_blocks = 2

        initial_state = State.get_state_from_value(qtd_blocks, '-WBBW')
        final_states = State.generate_final_states(qtd_blocks)

        bfs = BreadthFirstSearch(qtd_blocks, initial_state, final_states, True)

        open_queue = []

        s = initial_state
        open_queue.append(s)

        n = open_queue.pop(0)

        next_states = bfs._BreadthFirstSearch__generate_next_state(n)
        # open_queue = open_queue + next_states
        print(list(map(lambda state: state.value, next_states)))
        print(list(map(lambda state: state.value, open_queue)))

        pass


if __name__ == "__main__":
    unittest.main()
import unittest

try:
    import context
except ModuleNotFoundError:
    import tests.context

from app.state import State
from app.backtracking import Backtracking

class TestBacktrackingMethods(unittest.TestCase):
    def test_is_solution(self):
        qtd_blocks = 3

        initial_state = State.generate_initial_state(qtd_blocks)
        final_states = State.generate_final_states(qtd_blocks)

        testing_solution_state = State.get_state_from_value(qtd_blocks, 'WWWB-BB')
        
        bt = Backtracking(qtd_blocks, initial_state, final_states, True)
        is_solution = bt._Backtracking__is_solution(testing_solution_state)

        self.assertTrue(is_solution)

    def test_is_not_solution(self):
        qtd_blocks = 3

        initial_state = State.generate_initial_state(qtd_blocks)
        final_states = State.generate_final_states(qtd_blocks)

        testing_solution_state = State.get_state_from_value(qtd_blocks, 'WWB-BBW')
        
        bt = Backtracking(qtd_blocks, initial_state, final_states, True)
        is_solution = bt._Backtracking__is_solution(testing_solution_state)

        self.assertFalse(is_solution)

    def test_generate_new_states_3_pieces(self):
        qtd_blocks = 3

        initial_state = State.generate_initial_state(qtd_blocks)
        final_states = State.generate_final_states(qtd_blocks)

        bt = Backtracking(qtd_blocks, initial_state, final_states, True)

        n = initial_state

        n = bt._Backtracking__generate_states(n)
        self.assertEqual(n.value, 'BB-BWWW')

        n = bt._Backtracking__generate_states(n)
        self.assertEqual(n.value, 'BBWB-WW')

        n = bt._Backtracking__generate_states(n)
        self.assertEqual(n.value, 'B-WBBWW')

        n = bt._Backtracking__generate_states(n)
        self.assertEqual(n.value, 'BWWBB-W')

    def test_generate_new_states_2_pieces(self):
        qtd_blocks = 2

        initial_state = State.generate_initial_state(qtd_blocks)
        final_states = State.generate_final_states(qtd_blocks)

        bt = Backtracking(qtd_blocks, initial_state, final_states, True)

        n = initial_state

        n = bt._Backtracking__generate_states(n)
        self.assertEqual(n.value, 'B-BWW')

        n = bt._Backtracking__generate_states(n)
        self.assertEqual(n.value, 'BWB-W')

        n = bt._Backtracking__generate_states(n)
        self.assertEqual(n.value, '-WBBW')


if __name__ == "__main__":
    unittest.main()
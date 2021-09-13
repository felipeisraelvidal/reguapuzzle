from typing import final
from app.state import State
from app.backtracking import Backtracking
import unittest

class TestStateMethods(unittest.TestCase):
    def test_is_solution(self):
        qtd_blocks = 3

        initial_state = State.generate_initial_state(qtd_blocks)
        final_states = State.generate_final_states(qtd_blocks)

        testing_solution_state = State.get_state_from_value(qtd_blocks, 'WWWB-BB')
        
        bt = Backtracking(qtd_blocks, initial_state, final_states)
        is_solution = bt._Backtracking__is_solution(testing_solution_state)

        self.assertTrue(is_solution)

    def test_is_not_solution(self):
        qtd_blocks = 3

        initial_state = State.generate_initial_state(qtd_blocks)
        final_states = State.generate_final_states(qtd_blocks)

        testing_solution_state = State.get_state_from_value(qtd_blocks, 'WWB-BBW')
        
        bt = Backtracking(qtd_blocks, initial_state, final_states)
        is_solution = bt._Backtracking__is_solution(testing_solution_state)

        self.assertFalse(is_solution)

if __name__ == "__main__":
    unittest.main()
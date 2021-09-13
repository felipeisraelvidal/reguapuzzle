import unittest
from app.state import State

class TestStateMethods(unittest.TestCase):
    def test_initial_state(self):
        initial_state = State.generate_initial_state(2)
        self.assertEqual(initial_state.value, 'BB-WW')
        self.assertEqual(initial_state.id_parent, None)

        initial_state = State.generate_initial_state(3)
        self.assertEqual(initial_state.value, 'BBB-WWW')

    def test_final_states(self):
        final_states = State.generate_final_states(2)
        self.assertEqual(len(final_states), 5)
        self.assertIn('-WWBB', final_states)
        self.assertIn('W-WBB', final_states)
        self.assertIn('WW-BB', final_states)
        self.assertIn('WWB-B', final_states)
        self.assertIn('WWBB-', final_states)

    def test_get_state_from_value(self):
        state_value = 'BBBBB-WWWWW'
        initial_state = State.get_state_from_value(5, state_value)
        self.assertIsNotNone(initial_state)

    def test_not_get__state_from_value_because_is_invalid(self):
        state_value = 'BBBBH-WWWW'
        initial_state = State.get_state_from_value(5, state_value)
        self.assertIsNone(initial_state)

    def test_valid_initial_state(self):
        state_value = 'BBBB-WWWW'
        is_valid = State.validate_initial_state(state_value, 4)
        self.assertTrue(is_valid)

    def test_invalid_initial_state(self):
        state_value = 'BBBB-WWWWW'
        is_valid = State.validate_initial_state(state_value, 4)
        self.assertFalse(is_valid)

if __name__ == "__main__":
    unittest.main()
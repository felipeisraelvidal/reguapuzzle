from re import S
from algorithm import Algorithm
from game_state import GameState

class Backtracking(Algorithm):
    algorithm_name = 'Backtracking'

    def __init__(self, qtd_blocks, initial_state, final_states):
        super().__init__(qtd_blocks, initial_state, final_states)

        self.empty_piece_pos = self.initial_state.value.find('-')

        print(self.empty_piece_pos)

    def __generate_states(self):
        return []

    def __is_solution(self, state):
        return state.value in self.final_states

    def __back_to_parent(self, state):
        return None

    def execute(self):
        s = self.initial_state
        n = s
        game_state = GameState.PLAYING

        while game_state == GameState.PLAYING:
            new_states = self.__generate_states();
            if len(new_states) > 0:
                n = new_states[0]
                if self.__is_solution(n):
                    game_state = GameState.SUCCESS
            else:
                if n.value == s.value:
                    game_state = GameState.FAIL
                else:
                    n = self.__back_to_parent(n)

        print('Finished Game: ', game_state)
from app.algorithm import Algorithm
from app.game_state import GameState
from app.state import State
from app.extensions import *
import time

class Backtracking(Algorithm):
    algorithm_name = 'Backtracking'

    __current_move = 'L'
    __current_distance = 1
    __initial_empty_index_pos = 0

    def __init__(self, qtd_blocks, initial_state, final_states, is_testing = False):
        super().__init__(qtd_blocks, initial_state, final_states, is_testing)

        self.__initial_empty_index_pos = self.initial_state.value.find('-')

    def __generate_states(self, state):
        if self.__current_distance - self.__initial_empty_index_pos > self.qtd_blocks:
            return None

        empty_index = state.value.find('-')

        if self.__current_move == 'L':
            if empty_index - self.__current_distance < 0:
                self.__current_move = 'R'
                self.__current_distance = self.__current_distance + 1
                
                return None
            
            new_state_value = state.value
            new_state_value = replacer(new_state_value, state.value[empty_index - self.__current_distance], empty_index)
            new_state_value = replacer(new_state_value, '-', empty_index - self.__current_distance)

            new_state = State.get_state_from_value(self.qtd_blocks, new_state_value, id_parent=state.id)

            self.__current_move = 'R'
            self.__current_distance = self.__current_distance + 1

            return new_state
        elif self.__current_move == 'R':
            if empty_index + self.__current_distance > len(state.value) - 1:
                self.__current_move = 'L'
                self.__current_distance = self.__current_distance + 1

                return None
            
            new_state_value = state.value
            new_state_value = replacer(new_state_value, state.value[empty_index + self.__current_distance], empty_index)
            new_state_value = replacer(new_state_value, '-', empty_index + self.__current_distance)

            new_state = State.get_state_from_value(self.qtd_blocks, new_state_value, id_parent=state.id)

            self.__current_move = 'L'
            self.__current_distance = self.__current_distance + 1

            return new_state

    def __is_solution(self, state):
        return state.value in self.final_states

    def __back_to_parent(self, state, stack):
        if state.id_parent != None:
            parent = stack[state.id_parent]
            return parent

    def __get_path(self, final_state, stack):
        arr = []
        n = final_state
        while n != None:
            arr.insert(0, n.value)
            n = self.__back_to_parent(n, stack)
        
        print("Path:")
        for state in arr:
            print(f'\t{state}')

    # TODO: Calcular a profundidade e o custo da solução
    # TODO: Calcular o número total de nós expandidos e visitados
    # TODO: Calcular o valor médio do fator de ramificação da árvore de busca
    def execute(self):
        s = self.initial_state
        n = s
        game_state = GameState.PLAYING

        stack = {}
        stack[n.id] = n

        start_time = time.time()

        while game_state == GameState.PLAYING:
            new_state = self.__generate_states(n);
            if new_state != None:
                n = new_state
                stack[n.id] = n
                if self.__is_solution(n):
                    game_state = GameState.SUCCESS
            else:
                if n.value == s.value:
                    game_state = GameState.FAIL
                else:
                    n = self.__back_to_parent(n, stack)

        stop_time = time.time()

        print('Finished Game: ', game_state)
        print(f'Execution time: {stop_time - start_time}s')
        
        self.__get_path(n, stack)

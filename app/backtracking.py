from app.algorithm import Algorithm
from app.game_state import GameState
from app.state import State
from app.extensions import *
from app.bcolors import bcolors
from app.output import Output
import time

class Backtracking(Algorithm):
    algorithm_name = 'Backtracking'

    __current_move = 'L'
    __current_distance = 1
    __initial_empty_index_pos = 0

    __final_state = None

    __qtd_visited_nodes = 0
    __qtd_expanded_nodes = 0

    __tree_height = 0

    def __init__(self, qtd_blocks, initial_state, final_states, is_testing = False):
        super().__init__(qtd_blocks, initial_state, final_states, is_testing)

        self.__initial_empty_index_pos = self.initial_state.value.find('-')

    def __generate_states(self, state):
        if self.__current_distance - self.__initial_empty_index_pos > self.qtd_blocks:
            return None

        empty_index = state.value.find('-')

        self.__tree_height = max([state.height, self.__tree_height])

        if self.__current_move == 'L':
            if empty_index - self.__current_distance < 0:
                self.__current_move = 'R'
                self.__current_distance = self.__current_distance + 1
                
                return None
            
            new_state_value = state.value
            new_state_value = replacer(new_state_value, state.value[empty_index - self.__current_distance], empty_index)
            new_state_value = replacer(new_state_value, '-', empty_index - self.__current_distance)

            new_state = State.get_state_from_value(self.qtd_blocks, new_state_value, id_parent=state.id, height=state.height + 1)

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

            new_state = State.get_state_from_value(self.qtd_blocks, new_state_value, id_parent=state.id, height=state.height + 1)

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

    def execute(self):
        s = self.initial_state
        n = s
        game_state = GameState.PLAYING

        stack = {}
        stack[n.id] = n

        start_time = time.time()

        while game_state == GameState.PLAYING:
            new_state = self.__generate_states(n);
            self.__qtd_visited_nodes = self.__qtd_visited_nodes + 1

            if new_state != None:
                n = new_state
                stack[n.id] = n
                self.__qtd_expanded_nodes = self.__qtd_expanded_nodes + 1
                if self.__is_solution(n):
                    self.__final_state = n
                    game_state = GameState.SUCCESS
            else:
                if n.value == s.value:
                    game_state = GameState.FAIL
                else:
                    n = self.__back_to_parent(n, stack)

        stop_time = time.time()

        color = bcolors.ENDC
        if game_state == GameState.SUCCESS:
            color = bcolors.OKGREEN
        elif game_state == GameState.FAIL:
            color = bcolors.FAIL
        
        if self.__final_state is not None:
            self.__get_path(self.__final_state, stack)

            print(f'Profundidade: {self.__final_state.height}')
        else:
            print('Path:\n\t-')
            print(f'Profundidade: -1')

        average_ramification_factor = self.__qtd_expanded_nodes / (self.__tree_height + 1)
        average_ramification_factor = round(average_ramification_factor, 2)

        execution_time = stop_time - start_time

        output = Output(self.algorithm_name, game_state, self.__qtd_expanded_nodes, self.__qtd_visited_nodes, average_ramification_factor, execution_time)
        
        print(f'Total de Nós Expandidos: {self.__qtd_expanded_nodes}')
        print(f'Total de Nós Visitados: {self.__qtd_visited_nodes}')
        print(f'Valor Médio do Fator de Ramificação da Árvore: {average_ramification_factor}')
        print(f'Execution time: {execution_time}s')
        
        print(f'{color}Finished Game: ', game_state, bcolors.ENDC)

        return output
from math import *
from app.extensions import *
from app.state import State
from app.game_state import GameState
from app.algorithm import Algorithm
from app.bcolors import bcolors
from app.output import Output
import time

class DepthFirstSearch(Algorithm):
    algorithm_name = 'Busca em Profundidade'

    __open_queue = []
    __open_dict = {}
    __closed_states_values = {}
    __closed_states_ids = {}

    _game_state = GameState.PLAYING
    __final_state = None

    __qtd_visited_nodes = 0
    __qtd_expanded_nodes = 0

    __tree_height = 0

    def __init__(self, qtd_blocks, initial_state, final_states, is_testing=False):
        super().__init__(qtd_blocks, initial_state, final_states, is_testing)

    def generate_next_states(self, state):
        new_height = state.height + 1

        current_distance = 1

        if state.value in self.__closed_states_values:
            return

        if new_height > 10 * self.qtd_blocks:
            return

        states = []
        for _ in range(self.qtd_blocks):
            empty_index = state.value.find('-')

            if current_distance <= self.qtd_blocks:
                # Mudar para a esquerda
                if empty_index - current_distance >= 0:
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index - current_distance],
                                               empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index - current_distance)

                    # print(f'-> {new_state_value}')
                    if new_state_value not in self.__closed_states_values and new_state_value not in self.__open_dict:
                        new_state = State(new_state_value, state.id, current_distance, height=state.height + 1)
                        self.__qtd_expanded_nodes = self.__qtd_expanded_nodes + 1

                        if self.__is_solution(new_state):
                            return new_state

                        states.append(new_state)

                # Mudar para a direita
                if empty_index + current_distance <= len(state.value) - 1:
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index + current_distance], empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index + current_distance)

                    if new_state_value not in self.__closed_states_values and new_state_value not in self.__open_dict:
                        new_state = State(new_state_value, state.id, current_distance, height=state.height + 1)
                        self.__qtd_expanded_nodes = self.__qtd_expanded_nodes + 1

                        if self.__is_solution(new_state):
                            return new_state

                        states.append(new_state)

                current_distance = current_distance + 1

        for state in reversed(states):
            self.__open_queue.insert(0, state)
            self.__open_dict[state.value] = True

    def __is_solution(self, state):
        return state.value in self.final_states

    def __push_into_open_queue(self, state):
        self.__open_queue.append(state)
        self.__open_dict[state.value] = True

    def __pop_from_open_queue(self, index):
        n = self.__open_queue.pop(index)
        if n.value in self.__open_dict:
            del self.__open_dict[n.value]
        return n

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
        self.__open_queue = []
        self.__open_dict = {}

        s = self.initial_state

        self._game_state = GameState.PLAYING
        self.__final_state = None

        # Insert s at open queue
        self.__push_into_open_queue(s)

        self.__closed_states_values = {}
        self.__closed_states_ids = {}

        start_time = time.time()

        while self._game_state == GameState.PLAYING:
            if len(self.__open_queue) == 0:
                self._game_state = GameState.FAIL
            else:
                n = self.__pop_from_open_queue(0)
                self.__qtd_visited_nodes = self.__qtd_visited_nodes + 1

                x = self.generate_next_states(n)
                if x != None:
                    self.__final_state = x
                    self._game_state = GameState.SUCCESS

                self.__closed_states_values[n.value] = n
                self.__closed_states_ids[n.id] = n

        stop_time = time.time()

        color = bcolors.ENDC
        if self._game_state == GameState.SUCCESS:
            color = bcolors.OKGREEN
        elif self._game_state == GameState.FAIL:
            color = bcolors.FAIL
        
        if self.__final_state is not None:
            self.__get_path(self.__final_state, self.__closed_states_ids)

            print(f'Profundidade: {self.__final_state.height}')
        else:
            print('Path:\n\t-')
            print(f'Profundidade: -1')

        average_ramification_factor = self.__qtd_expanded_nodes / (self.__tree_height + 1)
        average_ramification_factor = round(average_ramification_factor, 2)

        execution_time = stop_time - start_time

        output = Output(self.algorithm_name, self._game_state, self.__qtd_expanded_nodes, self.__qtd_visited_nodes, average_ramification_factor, execution_time)
        
        print(f'Total de Nós Expandidos: {self.__qtd_expanded_nodes}')
        print(f'Total de Nós Visitados: {self.__qtd_visited_nodes}')
        print(f'Valor Médio do Fator de Ramificação da Árvore: {average_ramification_factor}')
        print(f'Execution time: {stop_time - start_time}s')
        
        print(f'{color}Finished Game: ', self._game_state, bcolors.ENDC)

        return output
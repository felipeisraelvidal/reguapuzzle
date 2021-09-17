from app.algorithm import Algorithm
from app.game_state import GameState
from app.bcolors import bcolors
from app.extensions import *
from app.state import State
import time

class BreadthFirstSearch(Algorithm):
    algorithm_name = "Breadth First Search"
    
    __open_queue = []
    __open_dict = {}
    __closed_states_values = {}
    __closed_states_ids = {}

    _game_state = GameState.PLAYING
    __final_state = None

    _qtd_moves = 0

    def __generate_next_state(self, state, callback):
        current_distance = 1

        if state.value in self.__closed_states_values.values():
            return

        for _ in range(self.qtd_blocks):
            empty_index = state.value.find('-')

            if current_distance <= self.qtd_blocks:
                # Mudar para a esquerda
                if empty_index - current_distance >= 0:
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index - current_distance], empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index - current_distance)

                    new_state = State.get_state_from_value(self.qtd_blocks, new_state_value, state.id, height=state.height + 1)
                    callback(new_state)

                if empty_index + current_distance <= len(state.value) - 1: # Mudar para a direita
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index + current_distance], empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index + current_distance)

                    new_state = State.get_state_from_value(self.qtd_blocks, new_state_value, state.id, height=state.height + 1)
                    callback(new_state)

                current_distance = current_distance + 1

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
            if len(self.__open_queue) < 1: # the open queue is empty
                self._game_state = GameState.FAIL
            else:
                n = self.__pop_from_open_queue(0)

                if self._Algorithm__is_solution(n):
                    self.__final_state = n
                    self._game_state = GameState.SUCCESS
                else:
                    if n.value in self.__closed_states_values:
                        self.__final_state = n
                        self._game_state = GameState.SUCCESS
                    else:
                        def validate_new_state(state):
                            self._qtd_moves = self._qtd_moves + 1
                            # +1 nó gerado

                            if self._Algorithm__is_solution(state):
                                self.__final_state = state
                                self._game_state = GameState.SUCCESS
                            else:
                                if state.value not in self.__closed_states_values and state.value not in self.__open_dict:
                                    self.__push_into_open_queue(state)
                        
                        self.__generate_next_state(n, validate_new_state)
                        # +1 nó visitado
                        
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
        
        print(f'Custo da Solução:')
        print(f'Total de Nós Expandidos:')
        print(f'Total de Nós Visitados:')
        print(f'Valor Médio do Fator de Ramificação da Árvore:')
        print(f'Execution time: {stop_time - start_time}s')
        
        print(f'{color}Finished Game: ', self._game_state, bcolors.ENDC)
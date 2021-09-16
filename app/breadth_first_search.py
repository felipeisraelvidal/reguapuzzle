from app.algorithm import Algorithm
from app.game_state import GameState
from app.bcolors import bcolors
from app.extensions import *
from app.state import State
import time

class BreadthFirstSearch(Algorithm):
    algorithm_name = "Breadth First Search"
    
    __open_queue = []
    __closed_dict = {}

    _game_state = GameState.PLAYING

    def __generate_next_state(self, state, callback):
        current_distance = 1

        if state.value in self.__closed_dict.values():
            return

        for _ in range(self.qtd_blocks):
            empty_index = state.value.find('-')

            if current_distance <= self.qtd_blocks:
                # Mudar para a esquerda
                if empty_index - current_distance >= 0:
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index - current_distance], empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index - current_distance)

                    new_state = State.get_state_from_value(self.qtd_blocks, new_state_value, state.id)
                    callback(new_state)

                if empty_index + current_distance <= len(state.value) - 1: # Mudar para a direita
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index + current_distance], empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index + current_distance)

                    new_state = State.get_state_from_value(self.qtd_blocks, new_state_value, state.id)
                    callback(new_state)

                current_distance = current_distance + 1

    def __push_into_open_queue(self, state):
        self.__open_queue.append(state)

    def __pop_from_open_queue(self, index):
        n = self.__open_queue.pop(index)
        return n

    def execute(self):
        self.__open_queue = []

        s = self.initial_state

        self._game_state = GameState.PLAYING

        # Insert s at open queue
        self.__push_into_open_queue(s)

        self.__closed_dict = {}

        start_time = time.time()

        while self._game_state == GameState.PLAYING:
            if len(self.__open_queue) < 1: # the open queue is empty
                self._game_state = GameState.FAIL
            else:
                n = self.__pop_from_open_queue(0)

                if self._Algorithm__is_solution(n):
                    self._game_state = GameState.SUCCESS
                else:
                    print(f'\nTrying the {n.value}')
                    print(f'{n.value} is not a solution')

                    def validate_new_state(state):
                        print(state.value)
                        if self._Algorithm__is_solution(state):
                            self._game_state = GameState.SUCCESS
                        else:
                            if state.value not in self.__closed_dict:
                                self.__push_into_open_queue(state)
                    
                    self.__generate_next_state(n, validate_new_state)
                    self.__closed_dict[n.value] = n
                    
                    print('open_queue', list(map(lambda state: state.value, self.__open_queue)))
                    print('closed_queue', list(map(lambda state: state, self.__closed_dict.keys())))
        
        stop_time = time.time()
        
        color = bcolors.ENDC
        if self._game_state == GameState.SUCCESS:
            color = bcolors.OKGREEN
        elif self._game_state == GameState.FAIL:
            color = bcolors.FAIL
        
        print(f'{color}Finished Game: ', self._game_state, bcolors.ENDC)

        print(f'Execution time: {stop_time - start_time}s')
        # print(n.value)

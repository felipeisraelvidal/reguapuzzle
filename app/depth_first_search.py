from math import *
from app.extensions import *
from app.state import State
from app.game_state import GameState
from app.algorithm import Algorithm
import time


class DepthFirstSearch(Algorithm):
    algorithm_name = 'Depth First Search'

    def __init__(self, qtd_blocks, initial_state, final_states, is_testing=False):
        super().__init__(qtd_blocks, initial_state, final_states, is_testing)

    def generate_next_states(self, open_queue, close_list, open_queueSet):
        state = open_queue[0]
        new_height = state.height + 1

        current_distance = 1

        if state.value in close_list:
            return

        # if state.value in open_queueSet: #VALIDAR TB A LISTA DE ABERTO
        #      return

        if new_height > 10 * self.qtd_blocks:
            return

        states = []
        for _ in range(self.qtd_blocks):
            # for _ in range(self.qtd_blocks, 0, -1): #testando começar pelo maior
            empty_index = state.value.find('-')

            if current_distance <= self.qtd_blocks:
                # Mudar para a esquerda
                if empty_index - current_distance >= 0:
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index - current_distance],
                                               empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index - current_distance)

                    # print(f'-> {new_state_value}')
                    if new_state_value not in close_list:

                        if new_state_value not in open_queueSet:  # VALIDAR TB A LISTA DE ABERTO
                            new_state = State(new_state_value, None, new_height, current_distance)

                            if self.__is_solution(new_state):
                                return new_state

                            states.append(new_state)
                            # open_queue.append(new_state) # adiciona já diretamente na lista de abertos

                            # open_queueSet[new_state_value] = True  # ADICIONA VALOR NOVO NO SET DE ABERTOS

                # Mudar para a direita
                if empty_index + current_distance <= len(state.value) - 1:
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index + current_distance],
                                               empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index + current_distance)

                    if new_state_value not in close_list:

                        if new_state_value not in open_queueSet:  # VALIDAR TB A LISTA DE ABERTO
                            new_state = State(new_state_value, None, new_height, current_distance)

                            if self.__is_solution(new_state):
                                return new_state

                            states.append(new_state)
                            # open_queue.append(new_state) # adiciona já diretamente na lista de abertos

                            # open_queueSet[new_state_value] = True #ADICIONA VALOR NOVO NO SET DE ABERTOS

                current_distance = current_distance + 1

        for state in reversed(states):
            # print(state.value)
            open_queue.insert(0, state)
            open_queueSet[state.value] = True

    def __is_solution(self, state):
        return state.value in self.final_states

    def execute(self):
        open_queue = []
        close_list = {}

        open_queueSet = {}

        s = self.initial_state
        game_state = GameState.PLAYING

        open_queue.insert(0, s)

        open_queueSet[s.value] = True

        start_time = time.time()
        while game_state == GameState.PLAYING:
            if len(open_queue) == 0:
                game_state = GameState.FAIL
            else:
                n = open_queue[0]
                if self.__is_solution(n):
                    game_state = GameState.SUCCESS
                else:
                    n = self.generate_next_states(open_queue, close_list, open_queueSet)
                    if n != None:
                        game_state = GameState.SUCCESS

                    now_closed = open_queue.pop(0)
                    close_list[now_closed.value] = now_closed
                    # open_queueSet.remove(now_closed.value)

        stop_time = time.time()

        print(f'Execution time: {stop_time - start_time}')

        print(game_state)
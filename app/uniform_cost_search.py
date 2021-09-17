from math import *
from app.extensions import *
from app.state import State
from app.game_state import GameState
import time
from app.algorithm import Algorithm

class UniformCostSearch(Algorithm):
    algorithm_name = 'Uniform Cost Search'

    def __init__(self, qtd_blocks, initial_state, final_states, is_testing = False):
        super().__init__(qtd_blocks, initial_state, final_states, is_testing)

    def sortKeyFunc(self, e):
        return e.weight

    def generate_next_states(self, open_queue, close_list):
        state = open_queue[0]
        print('Estado Atual:')
        print(state.value)

        current_distance = 1

        if state.value in close_list:
            return

        for _ in range(self.qtd_blocks):
            empty_index = state.value.find('-')

            if current_distance <= self.qtd_blocks:
                # Mudar para a esquerda
                if empty_index - current_distance >= 0:
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index - current_distance],
                                               empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index - current_distance)

                    if new_state_value not in close_list:
                        split_new_state_value = new_state_value.split('-')
                        before = split_new_state_value[0].count('W')
                        after = split_new_state_value[1].count('W')

                        new_weight = state.weight + current_distance
                        new_state = State(new_state_value, state.id, new_weight, before, after)

                        if self.is_solution(new_state):
                            return new_state

                        open_queue.append(new_state)  # adiciona já diretamente na lista de abertos


                if empty_index + current_distance <= len(state.value) - 1:
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index + current_distance],
                                               empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index + current_distance)

                    if new_state_value not in close_list:
                        split_new_state_value = new_state_value.split('-')
                        before = split_new_state_value[0].count('W')
                        after = split_new_state_value[1].count('W')

                        new_weight = state.weight + current_distance
                        new_state = State(new_state_value, state.id, new_weight, before, after)

                        if self.is_solution(new_state):
                            return new_state

                        open_queue.append(new_state)  # adiciona já diretamente na lista de abertos


                current_distance = current_distance + 1


    def is_solution(self, state):
        return any(elem for elem in self.final_states if elem == state.value)

    def execute(self):
        open_queue = []
        close_list = {}

        open_queueSet = {}

        s = self.initial_state
        game_state = GameState.PLAYING

        open_queue.append(s)


        start_time = time.time()
        while game_state == GameState.PLAYING:
            if len(open_queue) == 0:
                game_state = GameState.FAIL
            else:
                n = open_queue[0]
                if self.is_solution(n):
                    game_state = GameState.SUCCESS
                else:
                    n = self.generate_next_states(open_queue, close_list)
                    if n != None:
                        game_state = GameState.SUCCESS

                    now_closed = open_queue.pop(0)
                    close_list[now_closed.value] = now_closed
                    open_queue.sort(key=self.sortKeyFunc)

        stop_time = time.time()

        print(f'Execution time: {stop_time - start_time}')

        print(game_state)

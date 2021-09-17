from app.algorithm import Algorithm
from app.extensions import *
from app.game_state import GameState
from app.state import State
from app.bcolors import bcolors
import time

class AStar(Algorithm):
    algorithm_name = 'A Star'

    __final_state = None
    __closed_states_ids = {}

    __qtd_visited_nodes = 0
    __qtd_expanded_nodes = 0
    __tree_height = 0

    def __init__(self, qtd_blocks, initial_state, final_states, is_testing=False):
        super().__init__(qtd_blocks, initial_state, final_states, is_testing)

    def __get_path(self, final_state, stack):
        arr = []
        n = final_state
        while n != None:
            arr.insert(0, n.value)
            n = self.__back_to_parent(n, stack)

        print("Path:")
        for state in arr:
            print(f'\t{state}')

    def __back_to_parent(self, state, stack):
        if state.id_parent != None:
            parent = stack[state.id_parent]
            return parent

    def sortKeyFunc(self, e):
        return e.weight

    def generate_next_states(self, open_queue, close_list, open_queueSet):
        state = open_queue[0]
        custom = state.w_before
        current_distance = 1
        height = state.height + 1

        if state.value in close_list:
            return

        self.__tree_height = max([height, self.__tree_height])

        self.__qtd_visited_nodes = self.__qtd_visited_nodes + 1

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
                        if new_state_value not in open_queueSet:  # VALIDAR TB A LISTA DE ABERTO
                            self.__qtd_expanded_nodes = self.__qtd_expanded_nodes + 1

                            new_weight = custom + self.heuristicFunction(new_state_value, current_distance)
                            new_state = State(new_state_value, state.id, new_weight, height, custom + current_distance)

                            if self.__is_solution(new_state):
                                self.__qtd_visited_nodes = self.__qtd_visited_nodes + 1
                                return new_state
                            open_queue.append(new_state)
                            open_queueSet[new_state_value] = True  # ADICIONA VALOR NOVO NO SET DE ABERTOS

                # Mudar para a direita
                if empty_index + current_distance <= len(state.value) - 1:
                    new_state_value = state.value
                    new_state_value = replacer(new_state_value, new_state_value[empty_index + current_distance], empty_index)
                    new_state_value = replacer(new_state_value, '-', empty_index + current_distance)

                    if new_state_value not in close_list:
                        if new_state_value not in open_queueSet:  # VALIDAR TB A LISTA DE ABERTO
                            self.__qtd_expanded_nodes = self.__qtd_expanded_nodes + 1

                            new_weight = custom + self.heuristicFunction(new_state_value, current_distance)
                            new_state = State(new_state_value, state.id, new_weight, height, custom + current_distance)

                            if self.__is_solution(new_state):
                                self.__qtd_visited_nodes = self.__qtd_visited_nodes + 1
                                return new_state

                            open_queue.append(new_state)
                            open_queueSet[new_state_value] = True #ADICIONA VALOR NOVO NO SET DE ABERTOS

                current_distance = current_distance + 1

    def __is_solution(self, state):
        return state.value in self.final_states

    def heuristicFunction(self, state, distance):
        dist = 0
        cout = 0
        delimiter = state.find('-') + self.qtd_blocks + 1;

        if state[2*self.qtd_blocks] == 'W' and delimiter < 2*self.qtd_blocks : return -30;
        if state[2 * self.qtd_blocks - 1] == 'W': return -10;

        for i in range(0,self.qtd_blocks):

            if state[i] == 'B':
                if dist <= self.qtd_blocks:
                    cout = cout + 1
                else:
                    cout = cout + 2
            elif i == '-':
                dist = dist - 1

        for i in range(self.qtd_blocks +1 , 2*self.qtd_blocks):

            if state[i] == 'W':
                if dist >= 2*self.qtd_blocks:
                    cout = cout + 4
                else:
                    cout = cout + 2
            elif i == '-':
                dist = dist - 1

        return cout + distance
    
    def execute(self):
        open_queue = []
        close_list = {}
        open_queueSet = {}
        s = self.initial_state
        game_state = GameState.PLAYING
        open_queue.append(s)
        open_queueSet[s.value] = True
        self.__closed_states_ids = {}

        start_time = time.time()
        while game_state == GameState.PLAYING:
            if len(open_queue) == 0:
                game_state = GameState.FAIL
            else:
                n = open_queue[0]
                if self.__is_solution(n):
                    self.__final_state = n
                    game_state = GameState.SUCCESS
                else:
                    n = self.generate_next_states(open_queue, close_list, open_queueSet)
                    if n != None:
                        self.__final_state = n
                        game_state = GameState.SUCCESS

                    now_closed = open_queue.pop(0)
                    close_list[now_closed.value] = now_closed
                    self.__closed_states_ids[now_closed.id] = now_closed
                    open_queue.sort(key=self.sortKeyFunc)
                    
        stop_time = time.time()

        color = bcolors.ENDC
        if game_state == GameState.SUCCESS:
            color = bcolors.OKGREEN
        elif game_state == GameState.FAIL:
            color = bcolors.FAIL

        if self.__final_state is not None:
            self.__get_path(self.__final_state, self.__closed_states_ids)

            print(f'Profundidade: {self.__final_state.height}')
        else:
            print('Path:\n\t-')
            print(f'Profundidade: -1')

        average_ramification_factor = self.__qtd_expanded_nodes / (self.__tree_height + 1)
        average_ramification_factor = round(average_ramification_factor, 2)

        print(f'Total de Nós Expandidos: {self.__qtd_expanded_nodes}')
        print(f'Total de Nós Visitados: {self.__qtd_visited_nodes}')
        print(f'Valor Médio do Fator de Ramificação da Árvore: {average_ramification_factor}')
        print(f'Execution time: {stop_time - start_time}s')
        print(f'{color}Finished Game: ', game_state, bcolors.ENDC)
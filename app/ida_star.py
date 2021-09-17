from app.state import State
from app.extensions import *
# from gamestate import GameState
from app.game_state import GameState
from app.state import State
import time
import math
import functools

class IDAstar():
    current_move = 'L'
    current_distance = 1
    empty_index_pos = 0
    patamar_old = -1
    patamar = 0

    __qtd_visited_nodes = 0
    __qtd_expanded_nodes = 0
    __tree_height = 0

    def __init__(self, qtd_blocks, initial_state, final_states):
        self.qtd_blocks = qtd_blocks
        self.initial_state = initial_state
        self.final_states = final_states
        self.empty_index_pos = initial_state.value.find('-')

        # print('Initial State:')
        # print(f' - Value: {self.initial_state.value}')
        # print(f' - Empty index at: {self.empty_index_pos}')

    def teste(self, state):
        if (self.current_distance - self.empty_index_pos > self.qtd_blocks):
            return None

        empty_index = state.value.find('-')

        # print('----------------------------------------')
        # print(f'-> {state.value}')
        # print(f'Empty piece at position {empty_index}')

        if self.current_move == 'L':
            # print(f'Move {self.current_distance} to left')

            if empty_index - self.current_distance < 1:
                return None

            # print('Current move: L')
            # print(f'Empty index: {empty_index}')
            # print(f'Current distance: {self.current_distance}')

            new_state_value = state.value
            new_state_value = replacer(new_state_value, state.value[empty_index - self.current_distance], empty_index)
            new_state_value = replacer(new_state_value, '-', empty_index - self.current_distance)

            new_state = State(new_state_value, state.id)
            # print(f'-> {new_state_value} ({new_state.id} - {new_state.parent})')

            self.current_move = 'R'
            self.current_distance = self.current_distance + 1

            # print('----------------------------------------')

            return new_state
        elif self.current_move == 'R':
            # print(f'Move {self.current_distance} to right')

            if empty_index + self.current_distance > len(state.value) - 1:
                return None

            # print('Current move: R')
            # print(f'Empty index: {empty_index}')
            # print(f'Current distance: {self.current_distance}')

            new_state_value = state.value
            new_state_value = replacer(new_state_value, state.value[empty_index + self.current_distance], empty_index)
            new_state_value = replacer(new_state_value, '-', empty_index + self.current_distance)

            new_state = State(new_state_value, state.parent)
            # print(f'-> {new_state_value} ({new_state.id} - {new_state.parent})')

            self.current_move = 'L'
            self.current_distance = self.current_distance + 1

            # print('----------------------------------------')

            return new_state

    def heuristicFunction(self, state):
        dist = 0
        cout = 0
        delimiter = state.find('-') + self.qtd_blocks + 1;

        if state[2*self.qtd_blocks] == 'W' and delimiter < 2*self.qtd_blocks : return -50;

        if state[2 * self.qtd_blocks - 1] == 'W': return -5;

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

        return cout

    def is_solution(self, state):
        return any(elem for elem in self.final_states if elem == state.value)

    def back_to_parent(self, state, stack):
        if state.parent != None:
            parent = stack[state.parent]
            return parent

    def execute(self):
        s = self.initial_state
        n = s

        self.patamar = self.heuristicFunction(s.value)
        self.patamar_old = -1

        stack = {}
        descartados = []

        stack[n.id] = n
        descartados.append(self.heuristicFunction(n.value))
        
        game_state = GameState.PLAYING

        print(f'n = {n.value}')
        while game_state == GameState.PLAYING:
            if self.patamar == self.patamar_old:
                game_state = GameState.FAIL
            else:
                fn = self.heuristicFunction(n.value)
                if self.is_solution(n) and fn <= self.patamar:
                    game_state = GameState.SUCCESS
                else:
                    if fn > self.patamar:
                        # inserir f(N) em dascartados
                        descartados.append(self.heuristicFunction(n.value))
                        n = self.back_to_parent(n, stack)
                        pass
                    next_state = self.teste(n)
                    if next_state != None:
                        n = next_state
                        stack[n.id] = n
                        fn = self.heuristicFunction(n.value)
                    else:
                        if n.value == s.value:
                            self.patamar_old = self.patamar
                            # min_state = functools.reduce(lambda state1, state2: state1 if self.heuristicFunction(state1.value) < self.heuristicFunction(state2.value) else state2, descartados[1:], descartados[0])
                            min_fn = min(descartados)
                            self.patamar = min_fn
                            # descartados.remove(min_fn)
                        else:
                            n = self.back_to_parent(n, stack)




                # next_state = self.teste(n)
                # if next_state != None:
                #     n = next_state
                #     stack[n.id] = n
                #     if self.is_solution(n) == True:
                #         game_state = GameState.SUCCESS
                # else:
                #     if n.value == s.value:
                #         game_state = GameState.FAIL
                #     else:
                #         state_Value = n.value
                #         n = self.back_to_parent(n, stack)
                #         print(f'bt  {state_Value} -> {n.value}')
                # print(f'n = {n.value}')


        print(game_state)
        print(len(descartados))
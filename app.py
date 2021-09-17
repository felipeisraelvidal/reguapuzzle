from app.greedy_search import GreedySearch
from app.depth_first_search import DepthFirstSearch
import json
from app.state import State
from app.backtracking import Backtracking
from app.breadth_first_search import BreadthFirstSearch
from app.uniform_cost_search import UniformCostSearch
from app.astar_search import AStar
import os

def clear_console():
    clear = lambda: os.system('clear')
    clear()

def write_output_file(output_file, output):
    output_file.write(f'{output.algorithm_name}:\n')
    output_file.write(f'Total de Nós Expandidos: {output.qtd_expanded_nodes}\n')
    output_file.write(f'Total de Nós Visitados: {output.qtd_visited_nodes}\n')
    output_file.write(f'Valor Médio do Fator de Ramificação da Árvore: {output.average_ramification_factor}\n')
    output_file.write(f'Execution time: {output.execution_time}s\n')
    output_file.write(f'Finished Game: {output.game_state}\n\n')

def main():
    clear_console()
    
    f = open('config/config.json')
    data = json.load(f)

    board_config = data.get('boards')

    output_file = open('dist/output.txt', 'w')

    for board in board_config:
        number_of_pieces = board.get('pieces')
        print(f'Number of pieces: ', number_of_pieces)

        initial_state = board.get('initial_state')
        if initial_state == None or initial_state == '':
            initial_state = State.generate_initial_state(number_of_pieces)
        else:
            print(initial_state)
            initial_state = State.get_state_from_value(number_of_pieces, initial_state)
            if initial_state == None:
                raise ValueError('Invalid initial state in config file')

        final_states = State.generate_final_states(number_of_pieces)
        
        print(f'Initial state:\n\t{initial_state.value}')

        print(f'Final states:')
        for state in final_states:
            print(f'\t{state}')

        output_file.write(f'Quantidade de Nós: {number_of_pieces}\n\n')

        bt = Backtracking(number_of_pieces, initial_state, final_states)
        output = bt.execute()

        write_output_file(output_file, output)

        bfs = BreadthFirstSearch(number_of_pieces, initial_state, final_states)
        output = bfs.execute()

        write_output_file(output_file, output)

        dfs = DepthFirstSearch(number_of_pieces, initial_state, final_states)
        output = dfs.execute()

        write_output_file(output_file, output)

        ucs = UniformCostSearch(number_of_pieces, initial_state, final_states)
        output = ucs.execute()

        write_output_file(output_file, output)

        gs = GreedySearch(number_of_pieces, initial_state, final_states)
        output = gs.execute()

        write_output_file(output_file, output)

        astar = AStar(number_of_pieces, initial_state, final_states)
        output = astar.execute()

        write_output_file(output_file, output)

        # idastar = IDAstar(number_of_pieces, initial_state, final_states)
        # idastar.execute()

    f.close()
    output_file.close()

if __name__ == "__main__":
    main()
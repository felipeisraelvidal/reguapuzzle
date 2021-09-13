import json
from app.state import State
from app.backtracking import Backtracking
import os

def clear_console():
    clear = lambda: os.system('clear')
    clear()

def main():
    clear_console()
    
    f = open('config/config.json')
    data = json.load(f)

    board_config = data.get('board')

    number_of_pieces = board_config.get('pieces')
    print(f'Number of pieces: ', number_of_pieces)

    initial_state = board_config.get('initial_state')
    if initial_state == None or initial_state == '':
        initial_state = State.generate_initial_state(number_of_pieces)
    else:
        initial_state = State.generate_initial_state_from_value(initial_state, number_of_pieces)
        if initial_state == None:
            raise ValueError('Invalid initial state in config file')

    final_states = State.generate_final_states(number_of_pieces)
    
    print(f'Initial state:\n\t{initial_state.value}')

    print(f'Final states:')
    for state in final_states:
        print(f'\t{state}')
    
    bt = Backtracking(number_of_pieces, initial_state, final_states)
    bt.execute()

    f.close()

if __name__ == "__main__":
    main()
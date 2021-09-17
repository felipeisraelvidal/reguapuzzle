import uuid
from app.extensions import *
import re

class State():

    def __init__(self, value, id_parent, weight, height = 0, w_before = 0):
        self.id = uuid.uuid1()
        self.value = value
        self.id_parent = id_parent
        self.weight = weight
        self.height = height
        self.w_before = w_before
    
    @staticmethod
    def generate_initial_state(qtd_blocks):
        """Return the State object with the generated value"""
        b = 'B'
        w = 'W'
        result_value = f'{b * qtd_blocks}-{w * qtd_blocks}'
        
        return State(result_value, None, 0)

    @staticmethod
    def get_state_from_value(qtd_blocks, value, id_parent = None, weight = 0, height = 0):
        b_group = "".join(re.findall(r'[B]', value))
        w_group = "".join(re.findall(r'[W]', value))
        if len(b_group) == len(w_group) == qtd_blocks:
            return State(value, id_parent, weight, height)

    @staticmethod
    def generate_final_states(qtd_blocks):
        """Return an array of strings with all possible final states"""
        w = 'W'
        b = 'B'
        generic_state = f'{w * qtd_blocks}{b * qtd_blocks}'

        final_states = set()

        num_of_iterations = (qtd_blocks * 2) + 1
        for index in range(num_of_iterations):
            new_state = insert_substr(generic_state, '-', index)
            final_states.add(new_state)
        
        return final_states

    @staticmethod
    def validate_initial_state(value, qtd_blocks):
        """Return True if the value is valid"""
        if len(value) != (qtd_blocks * 2) + 1:
            return False
        else:
            regex = r'([B]{2,})-([W]{2,})$'
            result = re.fullmatch(regex, value)
            if result != None and len(result.group(1)) == len(result.group(2)):
                return True
        return False

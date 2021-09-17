class Algorithm():
    def __init__(self, qtd_blocks, initial_state, final_states, is_testing = False):
        self.qtd_blocks = qtd_blocks
        self.initial_state = initial_state
        self.final_states = final_states
        self.is_testing = is_testing

        if is_testing == False and self.algorithm_name is not None and self.algorithm_name != '':
            title = f'Executando {self.algorithm_name}'
            self.title_len = len(title)

            delimiter_char = '='
            separator_char = '-'
            print(f'{delimiter_char * self.title_len}\n{title}\n{separator_char * self.title_len}')

    def execute(self):
        raise ValueError("execute function not implemented")

    def __is_solution(self, state):
        return state.value in self.final_states

    def __del__(self):
        if self.is_testing == False and self.algorithm_name is not None and self.algorithm_name != '':
            delimiter_char = '='
            print(f'{delimiter_char * self.title_len}')
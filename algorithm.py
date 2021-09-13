class Algorithm():
    def __init__(self, qtd_blocks, initial_state, final_states):
        self.qtd_blocks = qtd_blocks
        self.initial_state = initial_state
        self.final_states = final_states

        if self.algorithm_name is not None and self.algorithm_name != '':
            title = f'Welcome to {self.algorithm_name}'
            self.title_len = len(title)

            delimiter_char = '='
            separator_char = '-'
            print(f'{delimiter_char * self.title_len}\n{title}\n{separator_char * self.title_len}')

    def execute(self):
        raise ValueError("execute function not implemented")

    def __del__(self):
        if self.algorithm_name is not None and self.algorithm_name != '':
            delimiter_char = '='
            print(f'{delimiter_char * self.title_len}')
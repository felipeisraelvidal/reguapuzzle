class Output():
    def __init__(self, algorithm_name, game_state, qtd_expanded_nodes, qtd_visited_nodes, average_ramification_factor, execution_time):
        self.algorithm_name = algorithm_name
        self.game_state = game_state
        self.qtd_expanded_nodes = qtd_expanded_nodes
        self.qtd_visited_nodes = qtd_visited_nodes
        self.average_ramification_factor = average_ramification_factor
        self.execution_time = execution_time
import numpy as np
import random
import const


class Markov:

    def __init__(self, states: list[any], iterations: int, transitions: np.ndarray):
        self.transition_matrix = transitions
        print(states)
        print(transitions)

        self.obs_state_frequencies = list()
        self.obs_state_probs = list()
        self.theory_state_probs = list()
        self.theory_transitions = list()
        self.stationary_dist = list()

        self.nodes = list()
        self.edges = list()

        self.sequence = list()

        states_ct = len(states)

        # Run iterative simulation
        cur_state = 0
        initial_dist = np.array([1] + [0 for _ in range(0, states_ct - 1)])
        state_draw_bucket = [i for i in range(0, states_ct)]
        self.obs_state_frequencies.append(initial_dist)
        self.obs_state_probs.append(initial_dist)
        self.theory_state_probs.append(initial_dist)
        self.theory_transitions.append(self.transition_matrix)

        self.sequence.append(0)

        for i in range(0, iterations):
            tm_row = self.transition_matrix[cur_state]
            cur_state = random.choices(state_draw_bucket, weights=tm_row, k=1)[0]

            self.sequence.append(cur_state)

            last_obs = list(self.obs_state_frequencies[-1])
            last_obs[cur_state] += 1
            last_tm = self.theory_transitions[-1]
            cur_tm = np.matmul(last_tm, self.transition_matrix)
            cur_theory_dist = np.matmul(initial_dist, cur_tm)

            self.obs_state_frequencies.append(last_obs)
            self.obs_state_probs.append(last_obs / sum(last_obs))
            self.theory_state_probs.append(cur_theory_dist)
            self.theory_transitions.append(cur_tm)

        # Initialize nodes and edges
        self.nodes = [
            {
                'id': state,
                'label': state,
                'shape': 'dot',
                'size': const.NODE_SIZE,
                'font': const.NODE_FONT,
                'color': const.NODE_COLOR_IDLE
            }
            for state in states
        ]

        self.edges = [
            {
                'id': states[idx_from] + "__" + states[idx_to],
                'label': str(p_from_to),
                'from': states[idx_from],
                'to': states[idx_to],
                'width': const.EDGE_WIDTH,
                'arrows': {
                    'to': {
                        'enabled': True,
                    }
                },
                'color': const.EDGE_COLOR,
                'font': const.EDGE_FONT
            }
            for idx_from, state_transitions in enumerate(self.transition_matrix)
            for idx_to, p_from_to in enumerate(state_transitions) if p_from_to > 0
        ]

        # Stationary distn
        transition_matrix_transp = self.transition_matrix.T
        eigen_vals, eigen_vects = np.linalg.eig(transition_matrix_transp)

        # Find the indexes of the eigenvalues that are close to 1
        close_to_1_idx = np.isclose(eigen_vals, 1)

        # Select eigenvects close to 1
        target_eigenvect = eigen_vects[:, close_to_1_idx]
        target_eigenvect = target_eigenvect[:, 0]

        # Turn the eigenvector elements into probabilities
        # Added '.real' to fix approximation errors from eigenval/vec finding
        # A real (but maybe not unique) stn dist (i.e., left eigenvec for eigenval 1) is
        # guaranteed to exist for stochastic matrix, so this is close enough :v
        self.stationary_dist = (target_eigenvect / sum(target_eigenvect)).real

        # print(self.obs_state_frequencies)
        # print(self.obs_state_probs)
        # print(self.theory_state_probs)
        # print(self.theory_transitions)
        # print(self.stationary_dist)


if __name__ == '__main__':
    chain = Markov(['mcdonalds', 'tacobell', 'kfc', 'wendys'], 1000, np.array([
        [0.1, 0.2, 0, 0.7],  # Mcd's
        [0.25, 0.25, 0.5, 0],  # TB's
        [0, 0.2, 0.8, 0],  # InOut's
        [0.3, 0.5, 0, 0.2],  # KFC's
    ]))
    # Test

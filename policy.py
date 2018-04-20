import numpy as np
import random
from rl.policy import EpsGreedyQPolicy

class Policy(object):
    def __init__(self, world):
        self.world = world

    def action(self, obs):
        raise NotImplementedError()


class TestPolicy(Policy):
    def action(self, obs):
        return random.choice(obs)

class EpsGreedyQPolicyWithGuide(EpsGreedyQPolicy):
    def __init__(self, world, eps=.1):
        super(EpsGreedyQPolicyWithGuide, self).__init__()
        self.eps = eps
        self.world = world

    def select_action(self, q_values):
        """Return the selected action
        # Arguments
            q_values (np.ndarray): List of the estimations of Q for each action
        # Returns
            Selection action
        """
        assert q_values.ndim == 1
        nb_actions = q_values.shape[0]

        if np.random.uniform() < self.eps:

            try:
                a_star_action = self.world.policy_agents[0].finda()
                a_star_action_i = self.world.action_space.index(a_star_action)
            except:
                a_star_action_i = None

            if random.random() < 0.2 or a_star_action_i is None:
                action = np.random.random_integers(0, nb_actions - 1)
            else:
                action = a_star_action_i

        else:
            action = np.argmax(q_values)
            
        return action

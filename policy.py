import numpy as np
import random

class Policy(object):
    def action(self, obs):
        raise NotImplementedError()


class TestPolicy(Policy):
    def action(self, obs):
        return [random.choice(obs)]
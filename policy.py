import numpy as np
import random

class Policy(object):
    def __init__(self, world):
        self.world = world

    def action(self, obs):
        raise NotImplementedError()


class TestPolicy(Policy):
    def action(self, obs):
        return random.choice(obs)
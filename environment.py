import gym
from gym import spaces
from gym.envs.registration import EnvSpec
import numpy as np

# environment for all agents in the multiagent world
# currently code assumes that no agents will be created/destroyed at runtime!
class OneStepEnv(gym.Env):
    def __init__(self, world):

        self.world = world
        self.agents = self.world.policy_agents

        # configure spaces
        self.action_space = []
        self.observation_space = []

    def step(self, action_n):
        return self.world.step(action_n)

    def reset(self):
        # reset world
        self.world.reset()

    # render environment
    def render(self):
        self.world.render()

    def observe(self):
        return self.world.observe()

    def decide(self):
        return self.world.decide()

class TestEnv(OneStepEnv):
    def __init__(self, world):
        super().__init__(world)

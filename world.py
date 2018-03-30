import copy

class World(object):
    def __init__(self, Policy):
        self.policy_agents = []

        self.policy = Policy()

        # configure spaces
        self.action_space = []
        self.observation_space = []

    def step(self, action_n):
        raise NotImplementedError()

    def reset(self):
        # reset world
        raise NotImplementedError()

    # render environment
    def render(self):
        raise NotImplementedError()

    def observe(self):
        return copy.copy(self.observation_space)

class TestWorld(World):
    def __init__(self, Policy):
        super().__init__(Policy)

        self.policy_agents = ["Npa"]

        # configure spaces
        self.action_space = ["Left", "Right", "Up", "Down"]
        self.observation_space = ["Left", "Right", "Up", "Down"]

    def decide(self):
        return [self.policy.action(obs) for obs in self.observation_space]

    def step(self, action_n):
        action = action_n[0] # as there is only one agent
        return [copy.copy(self.observation_space)], [0], [False], ["Nothing"]

    def reset(self):
        # reset world
        self.agents = ["Npa"]

        # configure spaces
        self.action_space = ["Left", "Right", "Up", "Down"]
        self.observation_space = ["Left", "Right", "Up", "Down"]

    # render environment
    def render(self):
        print("render!")

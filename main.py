# this is for display currently!!!!

from environment import TestEnv
from policy import TestPolicy
from world import TestWorld
from time import sleep

w = TestWorld(TestPolicy)
env = TestEnv(w)
obs_n = env.observe()
action_n = env.decide()
obs_n, reward_n, done_n, info_n = env.step(action_n)
while sum(done_n) != len(done_n):
    obs_n, reward_n, done_n, info_n = env.step(action_n)
    print(obs_n, reward_n, done_n, info_n)
    sleep(0.2)

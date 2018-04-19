import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPool2D, BatchNormalization
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from environment import OnePlayerEnv
from policy import EpsGreedyQPolicyWithGuide
from world import OneStepWorld
from time import sleep

ENV_NAME = 'CartPole-v0'


# Get the environment and extract the number of actions.
w = OneStepWorld(TestPolicy)
env = OnePlayerEnv(w)
np.random.seed(123)
env.seed(123)
nb_actions = len(env.action_space)

# print(env.observation_space.shape)
# exit()

# Next, we build a very simple model.
model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation="relu", input_shape=(1, ) + env.observation_space.shape,
                    data_format="channels_first"))
model.add(MaxPool2D(2, 2)),
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation="relu"))
model.add(MaxPool2D(2, 2))
model.add(Flatten())
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dense(32))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
model.summary()

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
policy = EpsGreedyQPolicyWithGuide(w)


# def money_patched_foo(self, state):
#     # state = np.array(state)
#     # state = np.reshape(state, state.shape[1: ])
#     # print(state.shape)
#     # exit()
#     q_values = self.compute_batch_q_values([state]).flatten()
#     assert q_values.shape == (self.nb_actions,)
#     return q_values
# DQNAgent.compute_q_values = money_patched_foo

dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=1000,
               target_model_update=1e-2, policy=policy)

dqn.compile(Adam(lr=1e-3), metrics=['mse'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)

# After training is done, we save the final weights.
# dqn.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=5, visualize=False)

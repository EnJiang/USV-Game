# this is for display currently!!!!

from environment import OnePlayerEnv
from policy import TestPolicy
from world import *
from time import sleep
from time import time as now

import random
import numpy as np

import gym
from gym import wrappers

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate, Conv2D, MaxPool2D, AvgPool2D
from keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.core import Processor


class NpaProcessor(Processor):
    def __init__(self):
        pass

    def process_state_batch(self, batch):
        batch_size = batch.shape[0]
        unit_size = batch.shape[-3: ]
        new_size = (batch_size,) + unit_size
        # print(new_size)
        return np.reshape(batch, new_size)

EPISODES = 100000

if __name__ == "__main__":
    # env = gym.make('CartPole-v1')

    w = ContinuousDynamicWorld(TestPolicy, obsticle_moving=False)
    env = OnePlayerEnv(w)

    # Next, we build a very simple model.
    actor = Sequential()
    actor.add(Conv2D(filters=8, kernel_size=(3, 3), activation="relu", input_shape=(5, 100, 100),
                     data_format="channels_first"))
    actor.add(Conv2D(filters=2, kernel_size=(3, 3),
                     activation="relu", data_format="channels_first"))
    # actor.add(MaxPool2D(2, 2, data_format="channels_first"))
    actor.add(AvgPool2D(2, 2, data_format="channels_first"))
    actor.add(Flatten())
    actor.add(Dense(256))
    actor.add(Activation('relu'))
    actor.add(Dense(32))
    actor.add(Activation('relu'))
    actor.add(Dense(16))
    actor.add(Activation('tanh'))
    actor.add(Dense(2))
    actor.add(Activation('tanh'))
    actor.summary()

    action_input = Input(shape=(2,), name='action_input')
    observation_input = Input(
        shape=(5, 100, 100), name='observation_input')
    x = Conv2D(filters=8, kernel_size=(3, 3), activation="relu",
               data_format="channels_first")(observation_input)
    x = Conv2D(filters=2, kernel_size=(3, 3), activation="relu",
               data_format="channels_first")(x)
    # x = MaxPool2D(2, 2, data_format="channels_first")(x)
    x = AvgPool2D(2, 2, data_format="channels_first")(x)
    x = Flatten()(x)
    x = Dense(255)(x)
    x = Activation('relu')(x)
    x = Concatenate()([x, action_input])
    x = Dense(255)(x)
    x = Activation('relu')(x)
    x = Dense(32)(x)
    x = Activation('relu')(x)
    x = Dense(16)(x)
    x = Activation('sigmoid')(x)
    x = Dense(1)(x)
    x = Activation('linear')(x)
    critic = Model(inputs=[action_input, observation_input], outputs=x)
    critic.summary()

    def monkey_patching_forward(self, observation):
        state = self.memory.get_recent_state(observation)
        action = self.select_action(state)
        self.recent_observation = observation
        self.recent_action = action
        # print(self.step)

        # first check if we are in warming up, if so,
        # run the pre-defined path
        # or, if the warm up phrase is over, give a
        # random action
        if (self.step < self.nb_steps_warmup_actor):
            actor = w.policy_agents[0]
            Action = actor.action_class
            try:
                F, T = actor.pathGuide33()
            except:
                pass
            else:
                action = np.array([F, T])
                action = np.reshape(action, self.recent_action.shape)
                self.recent_action = action
                return action

        # warm up is over...
        if random.random() < 0.2:
            F = (random.random() - 0.5)
            T = (random.random() - 0.5)
            action = np.array([F, T])
            action = np.reshape(action, self.recent_action.shape)
            self.recent_action = action
            return action

        # return the predicted one
        return action
    DDPGAgent.forward = monkey_patching_forward

    memory = SequentialMemory(limit=100000, window_length=1)
    agent = DDPGAgent(nb_actions=2, actor=actor, critic=critic, critic_action_input=action_input,
                      memory=memory, nb_steps_warmup_critic=10000, nb_steps_warmup_actor=10000,
                      gamma=.99, target_model_update=1e-3, processor=NpaProcessor())

    agent.compile([Adam(lr=1e-4), Adam(lr=1e-4)], metrics=['mae'])
    # agent.load_weights('ddpg_{}_weights.h5f'.format("continous"))
    agent.fit(env, nb_steps=800000, visualize=False, verbose=2)

    # After training is done, we save the final weights.
    agent.save_weights('ddpg_{}_weights.h5f'.format(
        "continous_dynamic"), overwrite=True)

    # Finally, evaluate our algorithm for 5 episodes.
    agent.test(env, nb_episodes=5, visualize=False, nb_max_episode_steps=1000)

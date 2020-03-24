import gym
import socket
import math
import numpy as np
from gym_dingnet.envs.protocol import DingNetConnection, Action, Observation
from gym import error, spaces, utils
from gym.utils import seeding
from gym_dingnet.logging import log

STATE_SPACE = [i for i in range(255, 2240)]
STATE_SPACE_SIZE = len(STATE_SPACE)

TP_SPACE = [i for i in range(-160, -120)]
TP_SIZE = len(TP_SPACE)
SF_SPACE = [i for i in range(7, 13)]
SF_SIZE = len(SF_SPACE)
SR_SPACE = [i for i in range(1, 16)]
SR_SIZE = len(SR_SPACE)


def space_size(with_tp, with_sf, with_sr):
    size = 1
    if with_tp:
        size = size * TP_SIZE
    if with_sf:
        size = size * SF_SIZE
    if with_sr:
        size = size * SR_SIZE
    return size


class DingNetEnv(gym.Env):

    def __init__(self, with_tp, with_sf, with_sr):
        self.with_tp = with_tp
        self.with_sf = with_sf
        self.with_sr = with_sr
        self.connection = DingNetConnection()

    def get_action_from_numbercode(self, numbercode: int):
        tp, sf, sr = -120, 12, 15
        if self.with_sr:
            sr = 1 + (numbercode % SR_SIZE)
            numbercode = (numbercode - (numbercode % SR_SIZE)) / SR_SIZE
        if self.with_sf:
            sf = 7 + (numbercode % (SF_SIZE))
            numbercode = (numbercode - (numbercode % SR_SIZE)) / SF_SIZE
        if self.with_tp:
            tp = -160 + (numbercode % (TP_SIZE))
        return Action(int(tp), int(sf), int(sr))

    def step(self, numbercode: int):
        action = self.get_action_from_numbercode(numbercode)
        self.connection.send_action(action)
        observation = self.connection.get_observation()
        print(action.tp, action.sf, action.sr,
              observation.xpos, observation.reward)
        reward = observation.reward
        done = self.is_done(observation)
        return (np.array([observation.xpos]).astype(np.int32), reward, done, {})

    def reset(self):
        print("reset", "----", 189, 0.0)
        self.connection.reset()
        return np.array([189]).astype(np.int32)

    def render(self):
        pass

    def compute_reward(self, observation):
        return observation.reward

    def is_done(self, observation):
        return observation.xpos >= 2400


# Environments without sampling rate


class DingNetEnv_TP(DingNetEnv):

    action_space = gym.spaces.Discrete(space_size(True, False, False))
    observation_space = gym.spaces.Discrete(STATE_SPACE_SIZE)

    def __init__(self):
        super().__init__(True, False, False)


class DingNetEnv_SF(DingNetEnv):

    action_space = gym.spaces.Discrete(space_size(False, True, False))
    observation_space = gym.spaces.Discrete(STATE_SPACE_SIZE)

    def __init__(self):
        super().__init__(False, True, False)


class DingNetEnv_TP_SF(DingNetEnv):

    action_space = gym.spaces.Discrete(space_size(True, True, False))
    observation_space = gym.spaces.Discrete(STATE_SPACE_SIZE)

    def __init__(self):
        super().__init__(True, True, False)

# Environments with smapling rate


class DingNetEnv_SR(DingNetEnv):

    action_space = gym.spaces.Discrete(space_size(False, False, True))
    observation_space = gym.spaces.Discrete(STATE_SPACE_SIZE)

    def __init__(self):
        super().__init__(False, False, True)


class DingNetEnv_SR_TP(DingNetEnv):

    action_space = gym.spaces.Discrete(space_size(True, False, True))
    observation_space = gym.spaces.Discrete(STATE_SPACE_SIZE)

    def __init__(self):
        super().__init__(True, False, True)


class DingNetEnv_SR_SF(DingNetEnv):

    action_space = gym.spaces.Discrete(space_size(False, True, True))
    observation_space = gym.spaces.Discrete(STATE_SPACE_SIZE)

    def __init__(self):
        super().__init__(False, True, True)


class DingNetEnv_SR_TP_SF(DingNetEnv):

    action_space = gym.spaces.Discrete(space_size(True, True, True))
    observation_space = gym.spaces.Discrete(STATE_SPACE_SIZE)

    def __init__(self):
        super().__init__(True, True, True)

import gym
import socket
from gym_dingnet.envs.protocol import DingNetConnection, Action, Observation
from gym import error, spaces, utils
from gym.utils import seeding

STATE_SPACE = [i for i in range(255, 2240)]
STATE_SPACE_SIZE = len(STATE_SPACE)

TP_SPACE = [i for i in range(-120, -160)]
TP_SIZE = len(TP_SPACE)
SF_SPACE = [i for i in range(7, 12)]
SF_SIZE = len(SF_SPACE)
SR_SPACE = [i for i in range(1, 16)]
SR_SIZE = len(SR_SPACE)


def space_size(with_tp, with_sf, with_sr):
    size = 1
    if with_tp:
        size *= TP_SIZE
    if with_sf:
        size *= SF_SIZE
    if with_sr:
        size *= SR_SIZE
    return size


class DingNetEnv(gym.Env):

    def __init__(self, with_tp, with_sf, with_sr):
        self.with_tp = with_tp
        self.with_sf = with_sf
        self.with_sr = with_sr
        self.connection = DingNetConnection()

    def step(self, action):
        self.connection.send_action(action)
        observation = self.connection.get_observation()
        reward = self.compute_reward(observation)
        done = self.is_done(observation)
        return (observation, reward, done, None)

    def reset(self):
        self.connection.reset()

    def render(self):
        pass

    def compute_reward(self, observation):
        return 0.0

    def is_done(self, observation):
        return False

    def close(self):
        self.connection.close()

# Environments without sampling rate


class DingNetEnv_TP(DingNetEnv):

    action_space = space_size(True, False, False)
    observation_space = STATE_SPACE_SIZE

    def __init__(self):
        super().__init__(True, False, False)


class DingNetEnv_SF(DingNetEnv):

    action_space = space_size(False, True, False)
    observation_space = STATE_SPACE_SIZE

    def __init__(self):
        super().__init__(False, True, False)


class DingNetEnv_TP_SF(DingNetEnv):

    action_space = space_size(True, True, False)
    observation_space = STATE_SPACE_SIZE

    def __init__(self):
        super().__init__(True, True, False)

# Environments with smapling rate


class DingNetEnv_SR(DingNetEnv):

    action_space = space_size(False, False, True)
    observation_space = STATE_SPACE_SIZE

    def __init__(self):
        super().__init__(False, False, True)


class DingNetEnv_SR_TP(DingNetEnv):

    action_space = space_size(False, False, True)
    observation_space = STATE_SPACE_SIZE

    def __init__(self):
        super().__init__(True, False, True)


class DingNetEnv_SR_SF(DingNetEnv):

    action_space = space_size(False, True, True)
    observation_space = STATE_SPACE_SIZE

    def __init__(self):
        super().__init__(False, True, True)


class DingNetEnv_SR_TP_SF(DingNetEnv):

    action_space = space_size(True, True, True)
    observation_space = STATE_SPACE_SIZE

    def __init__(self):
        super().__init__(True, True, True)

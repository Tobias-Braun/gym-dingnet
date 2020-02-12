import gym
import socket
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
        self.action_space = spaces.Discrete(
            space_size(with_tp, with_sf, with_sr))
        self.observation_space = spaces.Discrete(STATE_SPACE_SIZE)
        self.connection = socket.socket()

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self):
        pass

    def close(self):
        self.connection.send

# Environments without sampling rate


class DingNetEnv_TP(DingNetEnv):
    def __init__(self):
        super().__init__(True, False, False)


class DingNetEnv_SF(DingNetEnv):
    def __init__(self):
        super().__init__(False, True, False)


class DingNetEnv_TP_SF(DingNetEnv):
    def __init__(self):
        super().__init__(True, True, False)

# Environments with smapling rate


class DingNetEnv_SR(DingNetEnv):
    def __init__(self):
        super().__init__(False, False, True)


class DingNetEnv_SR_TP(DingNetEnv):
    def __init__(self):
        super().__init__(True, False, True)


class DingNetEnv_SR_SF(DingNetEnv):
    def __init__(self):
        super().__init__(False, True, True)


class DingNetEnv_SR_TP_SF(DingNetEnv):
    def __init__(self):
        super().__init__(True, True, True)

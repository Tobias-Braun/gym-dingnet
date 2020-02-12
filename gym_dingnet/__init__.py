from gym.envs.registration import register

"""
On import of this package, the DingNet environments are registered
Each configuration gets a different environment.
7 environments are registered, one for each configuration.
"""


# Environments without sampling rate

register(
    id='dingnet-tp',
    entry_point='gym_dingnet.envs:DingNetEnv_TP',
)

register(
    id='dingnet-sf',
    entry_point='gym_dingnet.envs:DingNetEnv_TP',
)

register(
    id='dingnet-tp-sf',
    entry_point='gym_dingnet.envs:DingNetEnv_TP_SF',
)

# Environments with sampling rate

register(
    id='dingnet-sr',
    entry_point='gym_dingnet.envs:DingNetEnv_SR',
)

register(
    id='dingnet-sr-tp',
    entry_point='gym_dingnet.envs:DingNetEnv_SR_TP',
)

register(
    id='dingnet-sr-sf',
    entry_point='gym_dingnet.envs:DingNetEnv_SR_SF',
)

register(
    id='dingnet-sr-tp-sf',
    entry_point='gym_dingnet.envs:DingNetEnv_SR_TP_SF',
)

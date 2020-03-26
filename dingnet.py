import gym
import gym_dingnet
from stable_baselines import PPO2
from gym_dingnet.logging import log
env = gym.make("dingnet-sr-tp-sf-v0")
print("training")
model = PPO2('MlpLstmPolicy', env, verbose=0, nminibatches=1).learn(50000000,)
print("done training")
obs = env.reset()
n_steps = 20
for step in range(n_steps):
    action, _ = model.predict(obs, deterministic=True)
    log("Step {}\n".format(step + 1))
    log("Action: {}\n".format(action))
    obs, reward, done, info = env.step(action)
    log(f'obs={obs}reward={reward} done={done}\n')
    env.render(mode='console')
    if done:
        # Note that the VecEnv resets automatically
        # when a done signal is encountered
        log(f'Goal reached!, reward={reward}')
        break

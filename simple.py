import gymnasium as gym
from gym import spaces
import numpy as np

class MySim(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Discrete(2)

    def step(self, action):
        state = 1

        print("action", action)
        done = False
        if action == 2:
            reward = 1
            done = True
        else:
            reward = -1
        info = {}
        return np.array((action, 1), dtype=np.float32), reward, done, info, {}
    
    def reset(self):
        state = 0
        # 初始化 state 的状态，在 step 中通过 x, z = self.state获取
        # 所以这里的参数个数与 step 需要的一致
        return np.array((1, 2), dtype=np.float32), {}
    
    def render(self, mode='human'):
        pass

    def seed(self, seed=None):
        pass
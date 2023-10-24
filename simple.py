import gymnasium as gym
from gym import spaces
import numpy as np

from lupa import LuaRuntime


class MySim(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(2)
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute('require("game")')
        self.call_lua = self.lua.globals()._G.call_lua
        self.call_lua("init")

    def step(self, action):
        state, reward, is_done = self.call_lua("step", action)
        # print("sate: ", state[1], state[2], reward)
        return np.array((state[1], state[2]), dtype=np.float32), reward, is_done, {}, {}
    
    def reset(self):
        # 初始化 state 的状态，在 step 中通过 x, z = self.state获取
        # 所以这里的参数个数与 step 需要的一致
        state = self.call_lua("reset")
        return np.array((state[1], state[2]), dtype=np.float32), {}
    
    def render(self, mode='human'):
        pass

    def seed(self, seed=None):
        pass
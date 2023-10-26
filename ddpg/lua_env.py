import gymnasium as gym
from gym import spaces
import numpy as np

from lupa import LuaRuntime


class CustomEnv(gym.Env):
    def __init__(self, file):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(2)
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute('require("{file}")'.format(file = file))
        self.call_lua = self.lua.globals()._G.call_lua
        action, observ = self.call_lua("init")
        print("box ========low", self.lua.table_from(action.low).values(), action.low.items())
        return self.conver_box(action), self.conver_box(observ)

    def conver_box(self, lua_box):
        return spaces.Box(low = lua_box.low.values(), high = lua_box.high.values(), dtype=np.float32)
        
#         Box(-1.0, 2.0, (3, 4), float32)
# Independent bound for each dimension:

# Box(low=np.array([-1.0, -2.0]), high=np.array([2.0, 4.0]), dtype=np.float32)
# Box([-1. -2.], [2. 4.], (2,), float32)
        
#     观测空间 = Box([-1. -1. -8.], [1. 1. 8.], (3,), float32)
# 动作空间 = Box(-2.0, 2.0, (1,), float32)
    def step(self, action):
        state, reward, is_done = self.call_lua("step", action)
        # print("sate: ", state[1], state[2], reward)
        return state.values(), reward, is_done, {}, {}
    
    def reset(self):
        # 初始化 state 的状态，在 step 中通过 x, z = self.state获取
        # 所以这里的参数个数与 step 需要的一致
        state = self.call_lua("reset")
        return state.values()
        #return np.array((state[1], state[2]), dtype=np.float32), {}
    
    def render(self, mode='human'):
        pass

    def seed(self, seed=None):
        pass
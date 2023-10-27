import gymnasium as gym
from gym import spaces
import numpy as np

from lupa import LuaRuntime


class CustomEnv(gym.Env):
    def __init__(self, file):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute('require("{file}")'.format(file = file))
        self.call_lua = self.lua.globals()._G.call_lua
        action, observ = self.call_lua("init")
        self.action_space = self.conver_box(action)
        self.observation_space = self.conver_box(observ)

    def lua_list_to_array(self, list):
        ar = []
        for value in list.values():
            ar.append(value)
        return ar
    
    def lua_list_to_np(self, list):
        ar = []
        for value in list.values():
            ar.append(value)
        return np.array(ar)

    def conver_box(self, lua_box):
        return spaces.Box(low = np.float32(self.lua_list_to_np(lua_box.low)), high = np.float32(self.lua_list_to_np(lua_box.high)), dtype=np.float32)

    #gymnasium.Env.step(self, action: ActType) → tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]
    def step(self, action):
        state, reward, is_done = self.call_lua("step", float(action[0]), float(action[1]), float(action[2]))
        # print("sate: ", state[1], state[2], reward)
        return self.lua_list_to_array(state), reward, is_done, {}, {}
    
    def reset(self, seed):
        # 初始化 state 的状态，在 step 中通过 x, z = self.state获取
        # 所以这里的参数个数与 step 需要的一致
        state = self.call_lua("reset")
        return self.lua_list_to_array(state), {}
    
    def render(self, mode='human'):
        pass

    def seed(self, seed=None):
        pass
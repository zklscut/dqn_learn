local self = {}

local M = {}

-- return action_count, observer_shape(box)
function M.init()
    --- Box(low=-1.0, high=2.0, shape=(3, 4), dtype=np.float32)
    -- {←, →, ↑, ↓}
    self.map = {
        {5, 1, 5},
        {1, 2, 1},
        {0, 2, 4},
    }
    return {low = {-1, -1, -1}, high = {1, 1, 1}}, {low = {0, 0, 0}, high = {4, 4, 4}}
end

function M.reset()
    self.state = {0, 0, 0}
    self.reward = {}
    self.step_count = 0
    self.total_reward = 0
    self.action_list = {}
    return self.state 
end

local function get_reward()
    local x, y, z = math.floor(self.state[1]), math.floor(self.state[2]), math.floor(self.state[3])
    if not self.map[x] or not self.map[x][z] then
        return -1
    end

    local index = x * 10 + z
    if self.reward[index] then
        return 0
    end

    if self.map[x][z] == y then
        self.reward[index] = true
        return 1
    end

    return 0    
end

function M.step(action)
    local reward = -1
    local x, y, z = self.state[1], self.state[2], self.state[3]
    local ax, ay, az = action[1], action[2], action[3]
    self.state[1] = x + ax
    self.state[2] = y + ay
    self.state[3] = z + az
    reward = get_reward()

    self.step_count = self.step_count + 1
    local is_done = self.step_count >= 1000
    self.total_reward = self.total_reward + reward
    if is_done then
        print("total reward ===", self.total_reward)
    end
    return self.state, self.reward, is_done
end


function call_lua(func_name, ...)
    return M[func_name](...)
end


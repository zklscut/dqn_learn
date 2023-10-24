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
    return 4, {low = 1, high = 9, shape = {3, 3}}
end

function M.reset()
    self.state = {1, 1}
    self.reward = {}
    self.step_count = 0
    self.total_reward = 0
    self.action_list = {}
    return self.state 
end

local function get_reward()
    local x, z = self.state[1], self.state[2]
    local index = x * 10 + z
    if not self.reward[index] then
        self.reward[index] = true
        return self.map[x][z]
    else
        return 0
    end
end

function M.step(action)
    action = action + 1
    -- {←, →, ↑, ↓}
    local reward = -1
    local x, z = self.state[1], self.state[2]
    if action == 1 then
        if x > 1 then
            self.state[1] = x - 1
            reward = get_reward()
        end
    elseif action == 2 then
        if x < 3 then
            self.state[1] = x + 1
            reward = get_reward()
        end
    elseif action == 3 then
        if z < 3 then
            self.state[2] = z + 1
            reward = get_reward()
        end
    elseif action == 4 then
        if z > 1 then
            self.state[2] = z - 1
            reward = get_reward()
        end
    end

    self.step_count = self.step_count + 1
    local is_done = self.step_count >= 6
    self.action_list[#self.action_list + 1] = action
    self.total_reward = self.total_reward + reward
    -- if is_done then
    --     print("actions: ", table.concat(self.action_list, ", "))
    --     print("total ==", self.total_reward)
    -- end
    return self.state, self.total_reward, is_done
end


function call_lua(func_name, ...)
    return M[func_name](...)
end


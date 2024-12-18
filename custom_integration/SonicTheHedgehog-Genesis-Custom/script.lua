-- Verificado
level_max_x = {
    -- Green Hill Zone
    ["zone=0,act=0"] = 0x2560,
    ["zone=0,act=1"] = 0x1F60,
    ["zone=0,act=2"] = 0x292A,

    -- Marble Zone
    ["zone=2,act=0"] = 0x1860,
    ["zone=2,act=1"] = 0x1860,
    ["zone=2,act=2"] = 0x1720,

    -- Spring Yard Zone
    ["zone=4,act=0"] = 0x2360,
    ["zone=4,act=1"] = 0x2960,
    ["zone=4,act=2"] = 0x2B83,

    -- Labyrinth Zone
    ["zone=1,act=0"] = 0x1A50,
    ["zone=1,act=1"] = 0x1150,
    ["zone=1,act=2"] = 0x1CC4,

    -- Star Light Zone
    ["zone=3,act=0"] = 0x2060,
    ["zone=3,act=1"] = 0x2060,
    ["zone=3,act=2"] = 0x1F48,

    -- Scrap Brain Zone
    ["zone=5,act=0"] = 0x2260,
    ["zone=5,act=1"] = 0x1EE0,
    -- ["zone=5,act=2"] = 000000, -- no tiene un x máximo
}


-- Verificado
function level_key()
    return string.format("zone=%d,act=%d", data.zone, data.act)
end


-- Verificado
function clip(v, min, max)
    if v < min then
        return min
    elseif v > max then
        return max
    else
        return v
    end
end


-- Verificado
data.prev_lives = 3

data.useless_jumps = 0
data.last_jumping_state = false

function is_jumping()
    return data.onAir == 1
end

-- Verificado
function contest_done()
    if data.lives < data.prev_lives then
        return true
    end
    data.prev_lives = data.lives

    if calc_progress(data) >= 1 then
        return true
    end

    return false
end


-- Verificado
data.offset_x = nil
end_x = nil


-- Verificado
function calc_progress(data)
    if data.offset_x == nil then
        data.offset_x = -data.x
        end_x = level_max_x[level_key()] - data.x
    end

    local cur_x = clip(data.x + data.offset_x, 0, end_x)
    return cur_x / end_x
end

data.prev_progress = 0
frame_limit = 18000
data.prev_rings = 0

function contest_reward()
    local progress = calc_progress(data)
    local speed_reward = math.max(data.speed_x, 0) * 0.05
    local reward = (progress - data.prev_progress) * 15000 + speed_reward

    local ring_diff = data.rings - data.prev_rings

    if ring_diff > 0 then
        reward = reward + ring_diff * 0.05
    end

    data.prev_rings = data.rings

    local currently_jumping = is_jumping()

    if currently_jumping then
        data.useless_jumps = data.useless_jumps + 1
    else
        data.useless_jumps = 0
    end

    local jump_penalty_threshold = 30
    if data.useless_jumps > jump_penalty_threshold then
        reward = reward - 1
    end

    data.prev_progress = progress

    if data.lives < data.prev_lives then
        reward = reward - 500
    end

    if currently_jumping and (progress > data.prev_progress) then
        reward = reward + 50
    end

    if progress >= 1 then
        reward = reward + 3000 + data.level_end_bonus
        local time_bonus = (1 - clip(scenario.frame / frame_limit, 0, 1)) * 2000
        reward = reward + time_bonus
    end

    return reward
end
import gymnasium as gym
import numpy as np
import struct
import json

class SelectRAM(gym.Wrapper):
    def __init__(self, env, selected_addresses, types, offset=-16711679):
        super(SelectRAM, self).__init__(env)
        self.selected_addresses = selected_addresses
        self.types = types
        self.offset = offset

        low = []
        high = []
        for t in self.types:
            if t == '|u1':
                low.append(0)
                high.append(255)
            elif t == '>u2':
                low.append(0)
                high.append(65535)
            elif t == '>i2':
                low.append(-32768)
                high.append(32767)
            elif t == '>u4':
                low.append(0)
                high.append(4294967295)
            else:
                raise ValueError(f"Tipo de dato no soportado: {t}")

        self.observation_space = gym.spaces.Box(
            low=np.array(low, dtype=np.float32),
            high=np.array(high, dtype=np.float32),
            dtype=np.float32
        )

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        selected_obs = self.extract_relevant_obs(obs)
        return selected_obs, info

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        selected_obs = self.extract_relevant_obs(obs)
        return selected_obs, reward, terminated, truncated, info

    def extract_relevant_obs(self, obs):
        selected_obs = []
        for address, dtype in zip(self.selected_addresses, self.types):
            adj_address = address + self.offset
            if dtype == '|u1':
                value = obs[adj_address]
            elif dtype == '>u2':
                byte_data = bytes(obs[adj_address:adj_address + 2])
                value = struct.unpack('>H', byte_data)[0]
            elif dtype == '>i2':
                byte_data = bytes(obs[adj_address:adj_address + 2])
                value = struct.unpack('>h', byte_data)[0]
            elif dtype == '>u4':
                byte_data = bytes(obs[adj_address:adj_address + 4])
                value = struct.unpack('>I', byte_data)[0]
            else:
                raise ValueError(f"Tipo de dato no soportado: {dtype}")

            selected_obs.append(value)
        return np.array(selected_obs, dtype=np.float32)


def load_data_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    array_selected = ["onAir", "screen_x", "screen_y", "speed_x", "speed_y", "x", "y"]
    selected_addresses = []
    types = []
    for key in sorted(data['info'].keys(), key=lambda k: data['info'][k]['address']):
        if key in array_selected:
            value = data['info'][key]
            selected_addresses.append(value['address'])
            types.append(value['type'])
    return selected_addresses, types

import gymnasium as gym
import numpy as np

class RestrictActions(gym.Wrapper):
    def __init__(self, env, allowed_actions):
        super(RestrictActions, self).__init__(env)
        self.allowed_actions = allowed_actions
        self.full_action_space = env.action_space
        self.action_space = gym.spaces.MultiBinary(len(allowed_actions))
        self.observation_space = env.observation_space

    def step(self, action):
        full_action = np.zeros(self.full_action_space.shape, dtype=action.dtype)
        for i, act_idx in enumerate(self.allowed_actions):
            full_action[act_idx] = action[i]
        obs, reward, terminated, truncated, info = self.env.step(full_action)
        return obs, reward, terminated, truncated, info

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)

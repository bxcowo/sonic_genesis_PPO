import gymnasium as gym

class FrameSkip(gym.Wrapper):
    def __init__(self, env, skip=4):
        super().__init__(env)
        self._skip = skip

    def step(self, act):
        total_rew = 0.0
        terminated = False
        truncated = False
        for i in range(self._skip):
            obs, rew, terminated, truncated, info = self.env.step(act)
            total_rew += rew
            if terminated or truncated:
                break

        return obs, total_rew, terminated, truncated, info

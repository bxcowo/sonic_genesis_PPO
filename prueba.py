import retro
import os
import numpy as np
import json

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv, VecNormalize
from stable_baselines3.common.callbacks import CheckpointCallback
from gymnasium.wrappers import FrameStackObservation
from Util_wrappers.SelectRam import SelectRAM, load_data_json
from Util_wrappers.FrameSkip import FrameSkip
from Util_wrappers.RestrictedActions import RestrictActions

curr_dir = os.path.dirname(os.path.abspath(__file__))
retro.data.Integrations.add_custom_path(os.path.join(curr_dir, "custom_integration"))

env = retro.RetroEnv(
    game='SonicTheHedgehog-Genesis-Custom',
    state=retro.State.DEFAULT,
    inttype=retro.data.Integrations.CUSTOM_ONLY,
    scenario='contest',
    obs_type=retro.Observations.RAM,
    render_mode="human"
)



data_json_path = os.path.join("custom_integration/SonicTheHedgehog-Genesis-Custom", 'data.json')
variables_name, selected_addresses, types = load_data_json(data_json_path)

env = SelectRAM(env, variables_name, selected_addresses, types)

print(env.observation_space)
print(env.action_space)

obs = env.reset()

for i in range(500):
    obs, rw, done, trunc, info = env.step(np.array([0, 0, 0, 0, 1]))
    print(obs)
    print(info)

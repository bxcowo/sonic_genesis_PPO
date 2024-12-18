import retro
import os

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.monitor import Monitor

from Util_wrappers.SelectRam import SelectRAM, load_data_json
from Util_wrappers.FrameSkip import FrameSkip
from Util_wrappers.RestrictedActions import RestrictActions
from gymnasium.wrappers import FrameStackObservation

# Function to create practice env, it has to be the same as the env defined in main.py with the same wrappers
def make_env_test():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    custom_integration_path = os.path.join(curr_dir, "custom_integration")
    retro.data.Integrations.add_custom_path(custom_integration_path)

    env = retro.RetroEnv(
        game='SonicTheHedgehog-Genesis-Custom',
        inttype=retro.data.Integrations.CUSTOM_ONLY,
        state=retro.State.DEFAULT,
        scenario='contest',
        obs_type=retro.Observations.RAM,
        render_mode="human",
        record=".",
    )

    env = FrameSkip(env, skip=4)
    data_json_path = os.path.join(custom_integration_path, 'SonicTheHedgehog-Genesis-Custom', 'data.json')
    selected_addresses, types = load_data_json(data_json_path)
    env = SelectRAM(env, selected_addresses, types)
    env = FrameStackObservation(env, stack_size=4)
    env = RestrictActions(env, [0, 4, 5, 6, 7])

    env = Monitor(env)

    return env

# Function to let the model play by itself
def main():
    MODEL_PATH = "sonic_model_final.zip"
    VEC_NORM_PATH = "vec_normalize.pkl"

    env = make_env_test()
    env = DummyVecEnv([lambda: env])

    curr_dir = os.path.dirname(os.path.abspath(__file__))
    custom_integration_path = os.path.join(curr_dir, "custom_integration")
    retro.data.Integrations.add_custom_path(custom_integration_path)

    vec_norm = VecNormalize.load(VEC_NORM_PATH, env)
    vec_norm.training = False
    vec_norm.norm_reward = False

    model = PPO.load(MODEL_PATH, env=vec_norm)

    obs = vec_norm.reset()

    done = False
    total_reward = 0
    step = 0
    max_steps = 100000

    try:
        while not done and step < max_steps:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = vec_norm.step(action)
            total_reward += reward
            step += 1
    finally:
        vec_norm.close()
        print(f"Recompensa total: {total_reward}")

if __name__ == '__main__':
    main()

import retro
import os

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv, VecNormalize
from stable_baselines3.common.callbacks import CheckpointCallback
from gymnasium.wrappers import FrameStackObservation
from Util_wrappers.SelectRam import SelectRAM, load_data_json
from Util_wrappers.FrameSkip import FrameSkip
from Util_wrappers.RestrictedActions import RestrictActions

def make_env():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    retro.data.Integrations.add_custom_path(os.path.join(curr_dir, "custom_integration"))

    env = retro.RetroEnv(
        game='SonicTheHedgehog-Genesis-Custom',
        inttype=retro.data.Integrations.CUSTOM_ONLY,
        state=retro.State.DEFAULT,
        scenario='contest',
        obs_type=retro.Observations.RAM,
        render_mode="human"
        )

    env = FrameSkip(env, skip=4)
    data_json_path = os.path.join("custom_integration/SonicTheHedgehog-Genesis-Custom", 'data.json')
    selected_addresses, types = load_data_json(data_json_path)
    env = SelectRAM(env, selected_addresses, types)
    env = FrameStackObservation(env, stack_size=4)
    env = RestrictActions(env, [0, 4, 5, 6, 7])
    return env

def main():
    num_envs = 4
    env = SubprocVecEnv([make_env for _ in range(num_envs)])
    env = VecNormalize(env, norm_obs=True, norm_reward=True, clip_obs=10.)

    model = PPO(
        policy="MlpPolicy",
        env=env,
        learning_rate=lambda f: f * 3e-4,
        n_steps=3200,
        batch_size=256,
        n_epochs=20,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.1,
        ent_coef=0.01,
        verbose=1,
    )

    checkpoint_callback = CheckpointCallback(save_freq=10000, save_path='modelos/',
                                             name_prefix='sonic_model')

    model.learn(
        total_timesteps=350_000,
        callback=checkpoint_callback,
        progress_bar=True
    )

    model.save("sonic_model_final")
    env.save("vec_normalize.pkl")


if __name__ == '__main__':
    main()

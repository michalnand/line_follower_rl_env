from gym.envs.registration import register
 
register(
    id='linefollower-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnv',
    max_episode_steps=4096, )

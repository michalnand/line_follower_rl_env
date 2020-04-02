from gym.envs.registration import register
 
register(
    id='linefollowerSimple-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnvSimpleFS1',
    max_episode_steps=16384, )


register(
    id='linefollowerSimple-v1', 
    entry_point='gym_linefollower.envs:LineFollowerEnvSimpleFS4',
    max_episode_steps=16384, )


register(
    id='linefollowerSimple-v2', 
    entry_point='gym_linefollower.envs:LineFollowerEnvSimpleFS8',
    max_episode_steps=16384, )


register(
    id='linefollowerAdvanced-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnvAdvancedFS1',
    max_episode_steps=16384, )


register(
    id='linefollowerAdvanced-v1', 
    entry_point='gym_linefollower.envs:LineFollowerEnvAdvancedFS4',
    max_episode_steps=16384, )


register(
    id='linefollowerAdvanced-v2', 
    entry_point='gym_linefollower.envs:LineFollowerEnvAdvancedFS8',
    max_episode_steps=16384, )


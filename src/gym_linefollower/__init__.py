from gym.envs.registration import register
 
register(
    id='linefollowerRawBasic-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnvRawBasic',
    max_episode_steps=16384, )

register(
    id='linefollowerRawAdvanced-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnvRawAdvanced',
    max_episode_steps=16384, )



register(
    id='linefollowerFrames1Basic-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnvFrames1Basic',
    max_episode_steps=16384, )

register(
    id='linefollowerFrames4Basic-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnvFrames4Basic',
    max_episode_steps=16384, )

register(
    id='linefollowerFrames8Basic-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnvFrames8Basic',
    max_episode_steps=16384, )




register(
    id='linefollowerFrames1Advanced-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnvFrames1Advanced',
    max_episode_steps=16384, )

register(
    id='linefollowerFrames4Advanced-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnvFrames4Advanced',
    max_episode_steps=16384, )

register(
    id='linefollowerFrames8Advanced-v0', 
    entry_point='gym_linefollower.envs:LineFollowerEnvFrames8Advanced',
    max_episode_steps=16384, )

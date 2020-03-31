import gym
import gym_linefollower

env = gym.make('linefollower-v0')

env.reset()
    
while True:
    action = env.action_space.sample()
    state, reward, done, _ = env.step(action)
    env.render()
		
    if done:
        env.reset()
import gym
import gym_linefollower

env = gym.make('linefollowerSimple-v0') #single line, state shape 1x96x96
#env = gym.make('linefollowerSimple-v1') #single line, state shape 4x96x96, 4 frames stacked
#env = gym.make('linefollowerSimple-v2') #single line, state shape 8x96x96, 8 frames stacked

'''
choose episodic random from 32 lines
black line white borad, or white line on black boars
'''
#env = gym.make('linefollowerAdvanced-v0') #episodic random from 32 lines, state shape 1x96x96
#env = gym.make('linefollowerAdvanced-v1') #episodic random from 32 lines, state shape 4x96x96, 4 frames stacked
#env = gym.make('linefollowerAdvanced-v2') #episodic random from 32 lines, state shape 8x96x96, 8 frames stacked


state = env.reset()
print("state_shape = ", state.shape)

steps = 0
games = 0
score = 0
    
while True:
    action = env.action_space.sample()
    state, reward, done, _ = env.step(action)

    #env.render()

    steps+= 1
    score+= reward
		
    if done:
        env.reset()
        games+= 1
    
    print("steps = ", steps, " games = ", games, " score = ", score)
    
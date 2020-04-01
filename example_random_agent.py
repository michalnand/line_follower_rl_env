import gym
import gym_linefollower
from matplotlib import pyplot as plt


#env = gym.make('linefollowerSimple-v0') #single line, state shape 1x96x96
#env = gym.make('linefollowerSimple-v1') #single line, state shape 4x96x96, 4 frames stacked
#env = gym.make('linefollowerSimple-v2') #single line, state shape 8x96x96, 8 frames stacked

'''
choose episodic random from 32 lines
black line white borad, or white line on black boars
'''
#env = gym.make('linefollowerAdvanced-v0') #episodic random from 32 lines, state shape 1x96x96
env = gym.make('linefollowerAdvanced-v1') #episodic random from 32 lines, state shape 4x96x96, 4 frames stacked
#env = gym.make('linefollowerAdvanced-v2') #episodic random from 32 lines, state shape 8x96x96, 8 frames stacked


state = env.reset()
print("state_shape = ", state.shape)

def draw_fig(rgb_data):
    plt.imshow(rgb_data, cmap='gray', aspect='equal')
    plt.pause(0.01)
    plt.close()
    
while True:
    action = env.action_space.sample()
    state, reward, done, _ = env.step(action)

    #draw_fig(state[0])
    env.render()
		
    if done:
        env.reset()
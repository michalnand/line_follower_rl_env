import gym
import gym_linefollower

env = gym.make('linefollowerRawBasic-v0') 
#env = gym.make('linefollowerRawAdvanced-v0')

#env = gym.make('linefollowerFrames1Basic-v0') #single line, state shape 1x96x96
#env = gym.make('linefollowerFrames4Basic-v0') #single line, state shape 4x96x96, 4 frames stacked
#env = gym.make('linefollowerFrames8Basic-v0') #single line, state shape 8x96x96, 8 frames stacked


#env = gym.make('linefollowerFrames1Advanced-v0') #episodic random from 32 lines, state shape 1x96x96
#env = gym.make('linefollowerFrames4Advanced-v0') #episodic random from 32 lines, state shape 4x96x96, 4 frames stacked
#env = gym.make('linefollowerFrames8Advanced-v0') #episodic random from 32 lines, state shape 8x96x96, 8 frames stacked


state = env.reset()
print("state_shape = ", state.shape)

steps = 0
games = 0
score = 0
    
while True:
    action = env.action_space.sample()
    state, reward, done, _ = env.step(action)

    env.render()

    steps+= 1
    score+= reward
		
    if done:
        env.reset()
        games+= 1

    print(state)
    print("steps = ", steps, " games = ", games, " score = ", score)


'''
state = env.reset()
print("state_shape = ", state.shape)

steps = 0
games = 0
score = 0
    
while True:

    print(state)
    e0 = state[0][0]
    e1 = state[0][1]
    print(e0, e1)

    base_speed = 0.2

    turn = 0.08*e0 + 1.8*(e0 - e1)


    lp = base_speed + turn
    rp = base_speed - turn

    state, reward, done, _ = env.step_continuous(lp, rp)

    print(e0, turn, lp, rp)

    env.render()

    steps+= 1
    score+= reward
  
		
    if done:
        env.reset()
        games+= 1

    print("steps = ", steps, " games = ", games, " score = ", score)
'''
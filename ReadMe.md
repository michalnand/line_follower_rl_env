# Line Follower reinforcement learning environment

<img src="./imgs/env.png" width="300" height="256">
<img src="./imgs/animation.gif" width="300" height="256">

### Observation
camera view from front of robot
- state : 4stacked grayscale frames, channels first, 4x96x96
- values float range <0.0, 1.0>

### TODO and bugs
- random lines
- remove rendering glitches !!!

 
### Actions 
discrete, 16 actions - powers to motors


### Reward
- +1 : for new path visited field, if more than 90% fields visited, episode done
- -1 : if more than 150mm away from line, episode ends
- small negative reward : for line position not in center

## Getting Started

#### random agent :

```python
import gym
import gym_linefollower

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
steps = 0
    
while True:
    action = env.action_space.sample()
    state, reward, done, _ = env.step(action)

    #draw_fig(state[0])
    env.render()

    print(steps)
    steps+= 1
		
    if done:
        env.reset()
```

### Prerequisites

numpy, gym, pybullet, opencv-python

### Installing

```bash
pip3 install -e .
```
import gym
import gym_linefollower

env = gym.make('linefollowerRawBasic-v0') 

state = env.reset()


target = 0.0
kp = 0.5
kd = 1.0

base_speed = 0.2



while True:
    line_now  = state[0][0] #current line position
    line_prev = state[0][1] #old line position
    
    errror_now  = target - line_now #erros
    errror_prev = target - line_now

    #PD controller
    turn = kp*errror_now + kp*(errror_now - errror_prev)

    left_motor_power  = base_speed - turn
    right_motor_power = base_speed + turn

    state, reward, done, _ = env.step_continuous(left_motor_power, right_motor_power)

    env.render()
		
    if done:
        env.reset()

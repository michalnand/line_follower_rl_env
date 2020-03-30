import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pybullet
import numpy
import time

from matplotlib import pyplot as plt
from gym import spaces


import pybullet_client
import track_generator
import line_follower_bot
import observation



class LineFollowerEnv(gym.Env):

    def __init__(self, frame_stacking = 4):

        self.dt = 1.0/200.0
        self.pi = 3.141592654


        self.pb_client = pybullet_client.Client(pybullet.DIRECT)
      
        self.line = track_generator.TrackGenerator(2048, 0.015)
        self.line.save("./line.obj")

        width  = 96
        height = 96

        self.obs = observation.Observation(width, height, frame_stacking)
        self.observation_space = spaces.Box(low=0, high=1.0, shape=(width, height, frame_stacking), dtype=numpy.float)
 
        self.action_space = spaces.Discrete(16)

        self.reset()

        self.actions = []

        self.actions.append([1.0, 0.0])
        self.actions.append([0.8, 0.0])
        self.actions.append([0.6, 0.0])
        self.actions.append([0.5, 0.0])
        self.actions.append([1.0, 0.9])
        self.actions.append([0.8, 0.6])
        self.actions.append([0.5, 0.4])
        self.actions.append([0.3, 0.1])

        self.actions.append([0.0, 1.0])
        self.actions.append([0.0, 0.8])
        self.actions.append([0.0, 0.6])
        self.actions.append([0.0, 0.5])
        self.actions.append([0.9, 1.0])
        self.actions.append([0.6, 0.8])
        self.actions.append([0.4, 0.5])
        self.actions.append([0.1, 0.3])



    def reset(self):

        self.pb_client.resetSimulation()
        self.pb_client.setGravity(0, 0, -9.81)
        self.pb_client.setTimeStep(self.dt)

        self.bot = line_follower_bot.LineFollowerBot(self.pb_client, "./motoko_uprising.urdf", "./track_plane.urdf", starting_point = self.line.get_start_random())

        self.left_power  = 0.0
        self.right_power = 0.0

        self.render_steps = 0

        self.observation = None
        self.reward      = 0.0
        self.done        = False
        self.info        = None

        self.visited_points = numpy.zeros(self.line.get_length(), dtype=bool)

        self.observation = self._update_observation()

        return self.observation


    def step(self, action):

        robot_x, robot_y, robot_z, pitch, roll, yaw = self.bot.get_position()

        l_pos, r_pos = self.bot.get_wheel_position()
        l_vel, r_vel = self.bot.get_wheel_velocity()
        l_tor, r_tor = self.bot.get_wheel_torque()


        left_power_target, right_power_target = self.actions[action]
        #left_power_target, right_power_target = 0.0, 0.0

        k = 0.05

        self.left_power   = (1.0 - k)*self.left_power + k*left_power_target
        self.right_power  = (1.0 - k)*self.right_power + k*right_power_target
    
        self.bot.set_throttle(self.left_power, self.right_power)
   
        self.pb_client.stepSimulation()


        closest_idx, closest_distance = self.line.get_closest(robot_x, robot_y)

        self.done   = False
        self.reward = 0.0


        #negative reward for not line following
        self.reward+= -1.0*numpy.clip(closest_distance*10.0, 0.0, 1.0)

        #positive reward for moving to next field
        if self.visited_points[closest_idx] == False:
            self.reward+= 1.0 
            self.visited_points[closest_idx] = True

        visited_count = numpy.sum(self.visited_points)

        if visited_count >= 0.9*self.line.get_length():
            self.done   = True
            self.reward = 1.0

        if closest_distance > 0.15:
            self.done   = True
            self.reward = -1.0

        self.observation = self._update_observation()
        
        return self.observation, self.reward, self.done, self.info
        


    def render(self):
        if self.render_steps%4 == 0:
            robot_x, robot_y, robot_z, pitch, roll, yaw = self.bot.get_position()

            width  = 256
            height = 256

            #image = bot.get_image(robot_x, robot_y, 0.2 + 2, robot_x, robot_y, 0)
            
            #top view
            top_view = self.bot.get_image(yaw*180.0/self.pi - 90, -90.0, 0.0, 2.3, robot_x, robot_y, robot_z, width = width, height = height)

            #third person view
            tp_view = self.bot.get_image(yaw*180.0/self.pi - 90, -40.0, 0.0, 0.1, robot_x + 0.02, robot_y, robot_z, width = width, height = height, fov=100)

            #camera view
            cam_view = self._get_camera_view()

            #sensor view
            dist = 0.05
            sensor_view = self.bot.get_image(yaw*180.0/self.pi - 90, -90.0, 0.0, 0.02, robot_x+dist*numpy.cos(yaw), robot_y+dist*numpy.sin(yaw), robot_z + 0.02, width = width, height = height, fov=100)

            image = numpy.vstack([numpy.hstack([top_view, tp_view]), numpy.hstack([cam_view, sensor_view])])

            image = numpy.clip(image, 0.0, 1.0)
        
            self._draw_fig(image)
        
        self.render_steps+= 1

    def _draw_fig(self, rgb_data):
        plt.rcParams['toolbar'] = 'None' 
        plt.style.use('dark_background')

        fig = plt.figure()
        #fig.set_size_inches(size)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        plt.set_cmap('hot')
        ax.imshow(rgb_data, aspect='equal')
        plt.pause(0.01)
        plt.close()

    def _get_camera_view(self, width = 256, height = 256):
        robot_x, robot_y, robot_z, pitch, roll, yaw = self.bot.get_position()
        return self.bot.get_image(yaw*180.0/self.pi - 90, -15.0, 0.0, 0.015, robot_x, robot_y, robot_z + 0.1, width = width, height = height, fov=60)

    def _update_observation(self):
        return self.obs.process(self._get_camera_view())
    



def draw_fig(rgb_data):
    plt.imshow(rgb_data, cmap='gray', aspect='equal')
    plt.pause(0.01)
    plt.close()




if __name__ == "__main__":

    env = LineFollowerEnv() #gym.make("BubbleShooter-v0")
    env.reset()
    env.render()
    
    while True:
        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        env.render()
		
        if done:
            env.reset()
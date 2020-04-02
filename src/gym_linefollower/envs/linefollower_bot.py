import numpy
import pybullet

class LineFollowerBot:
    def __init__(self, pb_client, model_file_name, starting_position):
        self.pb_client = pb_client

        orientation = self._to_quaternion(starting_position[1][0], 0.0, 0.0)

     
        self.bot_model = pybullet.loadURDF(model_file_name, basePosition = starting_position[0], baseOrientation = orientation, physicsClientId = self.pb_client)
        

        self.speed_max_rpm  = 1000.0

        self.speed_max     = self.speed_max_rpm*2.0*3.141592654/60.0

        self.left_velocity = 0.0
        self.right_velocity = 0.0
        
        self.left_wheel_joint   = 0
        self.right_wheel_joint  = 1

        self.set_throttle(0.0, 0.0)
        

    def set_throttle(self, left_power, right_power):

        vl, vr = self.get_wheel_velocity()

        self.left_velocity  =  vl + (left_power - vl/self.speed_max)*100.0
        self.right_velocity =  vr + (right_power - vr/self.speed_max)*100.0

        self._set_wheel_velocity(self.left_velocity, self.right_velocity)
   

    def get_wheel_position(self):
        l_pos, l_vel, l_react, l_torque = pybullet.getJointState(self.bot_model, self.left_wheel_joint, physicsClientId = self.pb_client)
        r_pos, r_vel, r_react, r_torque = pybullet.getJointState(self.bot_model, self.right_wheel_joint, physicsClientId = self.pb_client)
        return l_pos, r_pos

    def get_wheel_torque(self):
        l_pos, l_vel, l_react, l_torque = pybullet.getJointState(self.bot_model, self.left_wheel_joint, physicsClientId = self.pb_client)
        r_pos, r_vel, r_react, r_torque = pybullet.getJointState(self.bot_model, self.right_wheel_joint, physicsClientId = self.pb_client)
        return l_torque, r_torque

    def get_wheel_velocity(self):
        l_pos, l_vel, l_react, l_torque = pybullet.getJointState(self.bot_model, self.left_wheel_joint, physicsClientId = self.pb_client)
        r_pos, r_vel, r_react, r_torque = pybullet.getJointState(self.bot_model, self.right_wheel_joint, physicsClientId = self.pb_client)
        return l_vel, r_vel

    def get_position(self):
        position, orientation = pybullet.getBasePositionAndOrientation(self.bot_model, physicsClientId = self.pb_client)
        x, y, z = position
        orientation = pybullet.getEulerFromQuaternion(orientation, physicsClientId = self.pb_client)
        pitch, roll, yaw = orientation
        return x, y, z, pitch, roll, yaw

    

    def _set_wheel_velocity(self, left_velocity, right_velocity):

        pybullet.setJointMotorControl2(self.bot_model,
                                             jointIndex =   self.left_wheel_joint,
                                             controlMode=   pybullet.VELOCITY_CONTROL,
                                             targetVelocity      =   left_velocity,
                                             physicsClientId = self.pb_client)

        pybullet.setJointMotorControl2(self.bot_model,
                                             jointIndex =   self.right_wheel_joint,
                                             controlMode=   pybullet.VELOCITY_CONTROL,
                                             targetVelocity      =   right_velocity,
                                             physicsClientId = self.pb_client)
    
    def _to_quaternion(self, yaw, pitch, roll):
        cy = numpy.cos(yaw * 0.5)
        sy = numpy.sin(yaw * 0.5)
        cp = numpy.cos(pitch * 0.5)
        sp = numpy.sin(pitch * 0.5)
        cr = numpy.cos(roll * 0.5)
        sr = numpy.sin(roll * 0.5)

        x = cy * cp * sr - sy * sp * cr
        y = sy * cp * sr + cy * sp * cr
        z = sy * cp * cr - cy * sp * sr
        w = cy * cp * cr + sy * sp * sr

        return x, y, z, w



    def get_image(self, yaw, pitch, roll, distance, target_x, target_y, target_z, width = 512, height = 512, fov = 120):

        
        vm = pybullet.computeViewMatrixFromYawPitchRoll([target_x, target_y, target_z], distance, yaw, pitch, roll, 2, physicsClientId = self.pb_client)


        pm = pybullet.computeProjectionMatrixFOV(fov=fov,
                                                       aspect=width / height,
                                                       nearVal=0.0001,
                                                       farVal=10.1,
                                                       physicsClientId = self.pb_client) 

        w, h, rgb, deth, seg = pybullet.getCameraImage(width=width,
                                                             height=height,
                                                             viewMatrix=vm,
                                                             projectionMatrix=pm,
                                                             renderer=pybullet.ER_TINY_RENDERER,
                                                             physicsClientId = self.pb_client)

        rgb = numpy.array(rgb)
        rgb = rgb[:, :, :3]

        return rgb
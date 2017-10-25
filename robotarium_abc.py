import math
import time
from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines

import threading

import utilities.misc

class RobotariumABC(ABC):

    def __init__(self, number_of_agents=10, show_figure=True, save_data=True):

        self.number_of_agents = number_of_agents
        self.show_figure = show_figure
        self.save_data = save_data

        self.file_path = None
        self.current_file_size = 0

        # Constants
        self.max_linear_velocity = 0.1
        self.max_angular_velocity = 2*math.pi
        self.robot_size = 0.02
        self.time_step = 0.033

        self.velocities = np.zeros((2, number_of_agents))
        self.poses = utilities.misc.generate_initial_conditions(self.number_of_agents)
        self.saved_poses = []
        self.saved_velocities = []
        self.led_commands = []

        # Visualization
        self.figure = []
        self.axes = []
        self.arrow_patches = []
        self.circle_patches = []

        if(self.save_data):
            self.file_path = "robotarium_data_" + repr(int(round(time.time())))

        self.arrow_patches = []

        if(self.show_figure):
            self.figure, self.axes = plt.subplots()
            for i in range(number_of_agents):
                p = patches.Circle(self.poses[:2,i], self.robot_size, fill=False)
                front = patches.Circle(self.poses[:2,i]+0.5*np.array((self.robot_size*np.cos(self.poses[2,i]), self.robot_size*np.sin(self.poses[2,i]))),
                self.robot_size/3, fill=False)

                self.circle_patches.append(p)
                self.arrow_patches.append(front)
                self.axes.add_patch(p)
                self.axes.add_patch(front)

            # Draw arena
            self.axes.add_patch(patches.Rectangle((-6.5, -5.5), 13, 11, fill=False))

            self.axes.set_xlim(-6.5, 6.5)
            self.axes.set_ylim(-5.5, 5.5)

            plt.ion()
            plt.show()

    def set_velocities(self, ids, velocities):

        #Threshold linear velocities
        idxs = np.where(np.abs(velocities[0, :]) > self.max_linear_velocity)
        velocities[0, idxs] = self.max_linear_velocity*np.sign(velocities[0, idxs])

        # Threshold angular velocities
        idxs = np.where(np.abs(velocities[1, :]) > self.max_angular_velocity)
        velocities[1, idxs] = self.max_angular_velocity*np.sign(velocities[1, idxs])

        self.velocities = velocities

    @abstractmethod
    def call_at_scripts_end(self):
        pass

    @abstractmethod
    def get_poses(self):
        pass

    @abstractmethod
    def step(self):
        pass

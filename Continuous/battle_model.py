# model.py
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
import random
import copy
import numpy as np

import warrior_agent

class BattleModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, height):
        self.running = True
        self.space = ContinuousSpace(width, height, False)
        self.schedule = RandomActivation(self)

        # Create agents
        a = warrior_agent.RedWarrior(1, self)
        pos = np.array((1.0,5.0))
        self.schedule.add(a)
        self.space.place_agent(a, pos)

        a = warrior_agent.RedWarrior(3, self)
        pos = np.array((4.0,2.0))
        self.schedule.add(a)
        self.space.place_agent(a, pos)

        a = warrior_agent.BlueWarrior(2, self)
        pos = np.array((9.0,5.0))
        self.schedule.add(a)
        self.space.place_agent(a, pos)
        self.a = a

        a = warrior_agent.BlueWarrior(4, self)
        pos = np.array((6.0,1.0))
        self.schedule.add(a)
        self.space.place_agent(a, pos)
        self.a = a

    def step(self):
        self.schedule.step()
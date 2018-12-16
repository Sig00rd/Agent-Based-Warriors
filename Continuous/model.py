# model.py
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
import random
import copy
import numpy as np

class WarriorAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hp = 10

    def step(self):
        if self.hp <= 0:
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.move()
        
    def move(self):
        x,y = self.pos
        if self.type == 'blue':
            position = np.array([-1,0.0])
        elif self.type == 'red':
            position = np.array([1,0.0])
        new_pos = self.pos + position
        new_cell_agents = self.model.space.get_neighbors(new_pos,0)
        
        if(not self.model.space.out_of_bounds(new_pos)):
            if len(new_cell_agents) == 0:
                self.model.space.move_agent(self, new_pos)
            else:
                self.attack()

    def attack(self):
        x, y = self.pos
        if self.type == 'blue':
            position = np.array([-1,0.0])
        elif self.type == 'red':
            position = np.array([1,0.0])
        new_pos = self.pos + position
        cellmates = self.model.space.get_neighbors(new_pos,0)
        enemy = random.choice(cellmates)
        enemy.hp -= 1
        
class RedWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'red'
        
class BlueWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'blue'

class BattleModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, height):
        self.running = True
        self.space = ContinuousSpace(width, height, False)
        self.schedule = RandomActivation(self)

        # Create agents
        a = RedWarrior(1, self)
        pos = np.array((1.0,5.0))
        self.schedule.add(a)
        self.space.place_agent(a, pos)
        
        a = BlueWarrior(2, self)
        pos = np.array((9.0,5.0))
        self.schedule.add(a)
        self.space.place_agent(a, pos)
        self.a = a

    def step(self):
        self.schedule.step()
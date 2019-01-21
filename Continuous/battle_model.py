# model.py
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from math import floor
import random
import copy
import numpy as np

import warrior_agent

class BattleModel(Model):
    """A model with some number of agents."""
    def __init__(self, red_col,red_row,red_squad, blue_col,blue_row,blue_squad, red_movement, blue_movement, width, height):
        self.running = True
        self.space = ContinuousSpace(width, height, False)
        self.schedule = RandomActivation(self)
        self.next_agent_id = 1
        
        self.RED_MOVEMENT_SPEED = red_movement
        self.BLUE_MOVEMENT_SPEED = blue_movement

        separation_y = 1.2
        # Find center
        red_first_y = ((height/2 - (red_squad * red_row/2 * separation_y)) + separation_y/2) - ((red_squad-1) * separation_y/2)
        blue_first_y = ((height/2 - (blue_squad * blue_row/2 * separation_y)) + separation_y/2) - ((blue_squad-1) * separation_y/2)
        
        # Create agents
        self.spawner(1.0,red_first_y, 1.2,separation_y, red_col,red_row,red_squad, 'red')
        self.spawner(width - 1.0,blue_first_y, -1.2,separation_y, blue_col,blue_row,blue_squad, 'blue')
            
    def spawner(self, first_x, first_y, separation_x, separation_y, cols, rows, squad, type):
        for i in range(cols):
            for j in range(rows * squad):
                x = first_x + (separation_x * i)
                y = first_y + (separation_y * j)
                
                # Squad separator
                y = y + separation_y * (floor(j / rows))
                
                self.spawn(x,y,type)
        
        
    def spawn(self,x,y,type):
        if(type == 'red'):
            a = warrior_agent.RedWarrior(self.next_agent_id, self)
        else:
            a = warrior_agent.BlueCommonWarrior(self.next_agent_id, self)
        pos = np.array((x,y))
        self.schedule.add(a)
        self.space.place_agent(a, pos)

        self.next_agent_id += 1

    def step(self):
        self.schedule.step()
        print("Żywych agentów: "+str(len(self.schedule.agents)))
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
    def __init__(self, red_col,red_row,red_squad, blue_col,blue_row,blue_squad,blue_agents_elite_squad, red_movement, blue_movement, width, height):
        self.running = True
        self.space = ContinuousSpace(width, height, False)
        self.schedule = RandomActivation(self)
        self.next_agent_id = 1
        
        self.RED_MOVEMENT_SPEED = red_movement
        self.BLUE_MOVEMENT_SPEED = blue_movement

        separation_y = 1.5
        # Find center
        red_first_y = ((height/2 - (red_squad * red_row/2 * separation_y)) + separation_y/2) - ((red_squad-1) * separation_y*2)
        blue_first_y = ((height/2 - (blue_squad * blue_row/2 * separation_y)) + separation_y/2) - ((blue_squad-1) * separation_y*2)
        
        # Create agents
        self.spawner(15.0,red_first_y, 1.5,separation_y, red_col,red_row,red_squad,0, 'red')
        self.spawner(width - 15.0,blue_first_y, -1.5,separation_y, blue_col,blue_row,blue_squad,blue_agents_elite_squad, 'blue')
            
    def spawner(self, first_x, first_y, separation_x, separation_y, cols, rows, squad, elite_squad, type):
        for i in range(cols):
            for j in range(rows * squad):
                x = first_x + (separation_x * i)
                y = first_y + (separation_y * j)
                
                # Squad separator
                y = y + (4*separation_y) * (floor(j / rows))

                casual = squad - elite_squad
                if casual < 0:
                    casual = 0
                
                elite = True
                if casual > 0:
                    if squad-1 == floor(j / rows):
                        elite = False
                if casual > 1:
                    if floor(j / rows) == 0:
                        elite = False
                if casual > 2:
                    if squad-2 == floor(j / rows):
                        elite = False
                if casual > 3:
                    if floor(j / rows) == 1:
                        elite = False
                if casual == 5:
                    elite = False                
                
                self.spawn(x,y,type,elite)
        
        
    def spawn(self,x,y,type,elite):
        if(type == 'red'):
            a = warrior_agent.RedWarrior(self.next_agent_id, self)
        elif(elite == True):
            a = warrior_agent.BlueEliteWarrior(self.next_agent_id, self)
        else:
            a = warrior_agent.BlueCommonWarrior(self.next_agent_id, self)
        pos = np.array((x,y))
        self.schedule.add(a)
        self.space.place_agent(a, pos)

        self.next_agent_id += 1

    def step(self):
        self.schedule.step()
        print("Żywych agentów: "+str(len(self.schedule.agents)))
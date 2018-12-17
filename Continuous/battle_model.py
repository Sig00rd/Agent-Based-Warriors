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
		self.next_agent_id = 1

		# Create agents
		self.spawner(1.0,1.0, 1.2,1.2, 5,15, 'red')
		self.spawner(width - 1.0,1.0, -1.2,1.2, 5,15, 'blue')
			
	def spawner(self, first_x, first_y, separation_x, separation_y, cols, rows, type):
		for i in range(cols):
			for j in range(rows):
				x = first_x + (separation_x * i)
				y = first_y + (separation_y * j)
				self.spawn(x,y,type)
		
		
	def spawn(self,x,y,type):
		if(type == 'red'):
			a = warrior_agent.RedWarrior(self.next_agent_id, self)
		else:
			a = warrior_agent.BlueWarrior(self.next_agent_id, self)
		pos = np.array((x,y))
		self.schedule.add(a)
		self.space.place_agent(a, pos)

		self.next_agent_id += 1

	def step(self):
		self.schedule.step()
		print("Żywych agentów: "+str(len(self.schedule.agents)))
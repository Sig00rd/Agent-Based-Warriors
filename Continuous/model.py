# model.py
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
import random
import copy

class WarriorAgent(Agent):
	""" An agent with fixed initial wealth."""
	def __init__(self, unique_id, model):
		super().__init__(unique_id, model)
		self.hp = 10

	def step(self):
		if self.hp <= 0:
			self.model.grid.remove_agent(self)
			self.model.schedule.remove(self)
		else:
			self.move()
		
	def move(self):
		x,y = self.pos
		if self.type == 'blue':
			new_x = x-1
		elif self.type == 'red':
			new_x = x+1
		new_y = y
		new_cell_agents = self.model.grid.get_neighbors([new_x,new_y],0)
		if (new_x >= 0 and new_x < self.model.grid.width) and (new_y >= 0 and new_y < self.model.grid.height):
			if len(new_cell_agents) == 0:
				self.model.grid.move_agent(self, [new_x,new_y])
			else:
				self.attack()

	def attack(self):
		x, y = self.pos
		if self.type == 'blue':
			new_x = x-1
		elif self.type == 'red':
			new_x = x+1
		new_y = y
		cellmates = self.model.grid.get_neighbors([new_x,new_y],0)
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
		self.grid = ContinuousSpace(width, height, False)
		self.schedule = RandomActivation(self)

		# Create agents
		a = RedWarrior(1, self)
		self.schedule.add(a)
		self.grid.place_agent(a, (1, 5))
		
		a = BlueWarrior(2, self)
		self.schedule.add(a)
		self.grid.place_agent(a, (9, 5))
		self.a = a

	def step(self):
		self.schedule.step()
# model.py
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random


class WarriorAgent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hp = 10

    def step(self):
        self.move()
        if self.hp <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

    def move(self):
        x, y = self.pos
        if self.type == 'blue':
            new_x = x - 1
        elif self.type == 'red':
            new_x = x + 1
        if new_x >= 0:
            cellmates = self.model.grid.get_cell_list_contents((new_x, y))
            if len(cellmates) < 1:
                self.model.grid.move_agent(self, [new_x, y])
            else:
                self.attack()

    def attack(self):
        x, y = self.pos
        if self.type == 'blue':
            new_x = x - 1
        elif self.type == 'red':
            new_x = x + 1
        cellmates = self.model.grid.get_cell_list_contents((new_x, y))
        enemy = random.choice(cellmates)
        enemy.hp -= 1


class BlueWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'blue'


class RedWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'red'


class BattleModel(Model):
    """A model with some number of agents."""

    def __init__(self, width, height):
        self.running = True
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)

        # Create agents
        a = RedWarrior(1, self)
        self.schedule.add(a)
        self.grid.place_agent(a, (0, 5))

        a = BlueWarrior(2, self)
        self.schedule.add(a)
        self.grid.place_agent(a, (9, 5))

    def step(self):
        self.schedule.step()

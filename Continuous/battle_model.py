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

    def __init__(self, red_col, red_row, blue_col, blue_row, red_movement, blue_movement,
                 coherence_factor, separation_factor, match_factor, enemy_position_factor,
                 vision_range, flocking_radius, separation_distance, width, height):
        self.running = True
        self.space = ContinuousSpace(width, height, False)
        self.schedule = RandomActivation(self)
        self.next_agent_id = 1

        self.RED_MOVEMENT_SPEED = red_movement
        self.BLUE_MOVEMENT_SPEED = blue_movement
        self.COHERENCE_FACTOR = coherence_factor
        self.SEPARATION_FACTOR = separation_factor
        self.MATCH_FACTOR = match_factor
        self.ENEMY_POSITION_FACTOR = enemy_position_factor
        self.VISION_RANGE = vision_range
        self.FLOCKING_RADIUS = flocking_radius
        self.SEPARATION_DISTANCE = separation_distance

        # Create agents
        self.spawner(1.0, 1.0, 1.2, 1.2, red_col, red_row, 'red')
        self.spawner(width - 1.0, 1.0, -1.2, 1.2, blue_col, blue_row, 'blue')

    def spawner(self, first_x, first_y, separation_x, separation_y, cols, rows, type):
        for i in range(cols):
            for j in range(rows):
                x = first_x + (separation_x * i)
                y = first_y + (separation_y * j)
                self.spawn(x, y, type)

    def spawn(self, x, y, type):
        if type == 'red':
            a = warrior_agent.RedWarrior(self.next_agent_id, self)
        else:
            a = warrior_agent.BlueCommonWarrior(self.next_agent_id, self)
        pos = np.array((x, y))
        self.schedule.add(a)
        self.space.place_agent(a, pos)

        self.next_agent_id += 1

    def step(self):
        self.schedule.step()

        agents_and_allies_morale = []
        for agent in self.schedule.agent_buffer(False): #type: warrior_agent.WarriorAgent
            agents_and_allies_morale.append((agent, agent.get_average_morale_of_allies_in_flocking_radius()))

        for (agent, allies_morale) in agents_and_allies_morale: #type: (warrior_agent.WarriorAgent, float)
            agent.update_morale(agent.calculate_new_morale(allies_morale))

        print("Żywych agentów: " + str(len(self.schedule.agents)))


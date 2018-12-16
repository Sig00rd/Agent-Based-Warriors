import mesa.agent
import numpy as np
import random

import simulation_parameters

class WarriorAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hp = 10
        self.COHERENCE_FACTOR = simulation_parameters.COHERENCE_FACTOR
        self.MATCH_FACTOR = simulation_parameters.MATCH_FACTOR
        self.SEPARATION_FACTOR = simulation_parameters.SEPARATION_FACTOR
        self.ENEMY_POSITION_FACTOR = simulation_parameters.ENEMY_POSITION_FACTOR

    def step(self):
        if self.hp <= 0:
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.move()

    # def move(self):
    #     if self.type == 'blue':
    #         position = np.array([-1, 0.0])
    #     elif self.type == 'red':
    #         position = np.array([1, 0.0])
    #     new_pos = self.pos + position
    #     new_cell_agents = self.model.space.get_neighbors(new_pos, 0)
    #
    #     if not self.model.space.out_of_bounds(new_pos):
    #         if len(new_cell_agents) == 0:
    #             self.model.space.move_agent(self, new_pos)
    #         else:
    #             self.attack()
    def move(self):
        velocity_vector = self.calculate_move_vector()
        end_point = self.pos + velocity_vector * self.movement_speed
        self.model.space.move_agent(self, end_point)

    def calculate_move_vector(self):
        move_vector = (self.coherence_vector() * self.COHERENCE_FACTOR +
                       self.match_vector() * self.MATCH_FACTOR +
                       self.separate_vector() * self.SEPARATION_FACTOR +
                       self.enemy_position_vector() * self.ENEMY_POSITION_FACTOR)
        return move_vector

    def coherence_vector(self):
        pass

    def match_vector(self):
        pass

    def separate_vector(self):
        pass

    def enemy_position_vector(self):
        pass

    # def attack(self):
    #     if self.type == 'blue':
    #         position = np.array([-1, 0.0])
    #     elif self.type == 'red':
    #         position = np.array([1, 0.0])
    #     new_pos = self.pos + position
    #     cellmates = self.model.space.get_neighbors(new_pos, 2.0)
    #     enemy = random.choice(cellmates)
    #     enemy.hp -= 1


class RedWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'red'
        self.movement_speed = simulation_parameters.RED_MOVEMENT_SPEED

class BlueWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'blue'
        self.movement_speed = simulation_parameters.BLUE_MOVEMENT_SPEED
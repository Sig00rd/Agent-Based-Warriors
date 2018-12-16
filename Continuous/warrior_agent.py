import mesa.agent
import numpy as np
import random

import simulation_parameters

class WarriorAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hp = 10
        self.ENEMY_SCANNING_RADIUS = simulation_parameters.VISION_RANGE # promień widzenia przeciwników
        self.FLOCKING_RADIUS = simulation_parameters.FLOCKING_RADIUS # promień widzenia swoich
        self.SEPARATION_DISTANCE = simulation_parameters.SEPARATION_DISTANCE # promień w którym żołnierz chce być sam
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

    def move(self):
        visible_enemies = self.scan_for_enemies()
        visible_allies = self.scan_for_allies()

        velocity_vector = self.calculate_move_vector()
        normalised_velocity_vector = velocity_vector / np.linalg.norm(velocity_vector)
        end_point = self.pos + normalised_velocity_vector * self.movement_speed
        self.model.space.move_agent(self, end_point)

        move_vector = (self.coherence_vector(visible_allies) * self.COHERENCE_FACTOR +
                       self.match_vector(visible_allies) * self.MATCH_FACTOR +
                       self.separate_vector(visible_allies) * self.SEPARATION_FACTOR +
                       self.enemy_position_vector(visible_enemies) * self.ENEMY_POSITION_FACTOR)

        return move_vector

    def coherence_vector(self, visible_allies):
        return np.array([1.0, 1.0])

    def match_vector(self, visible_allies):
        return np.array([1.0, 1.0])

    def separate_vector(self, visible_allies):
        return np.array([1.0, 1.0])

    def enemy_position_vector(self, visible_enemies):
        return np.array([1.0, 1.0])

    def scan_for_allies(self):
        pass

    def scan_for_enemies(self):
        pass

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
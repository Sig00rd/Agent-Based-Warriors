import mesa.agent
import numpy as np
import random

import simulation_parameters

class WarriorAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hp = 10
        self.velocity = np.zeros(2)
        self.ENEMY_SCANNING_RADIUS = model.VISION_RANGE # promień widzenia przeciwników
        self.FLOCKING_RADIUS = model.FLOCKING_RADIUS # promień widzenia swoich
        self.SEPARATION_DISTANCE = model.SEPARATION_DISTANCE # jaki dystans chce zachować od innych w oddziale
        self.COHERENCE_FACTOR = model.COHERENCE_FACTOR
        self.MATCH_FACTOR = model.MATCH_FACTOR
        self.SEPARATION_FACTOR = model.SEPARATION_FACTOR
        self.ENEMY_POSITION_FACTOR = model.ENEMY_POSITION_FACTOR

    def step(self):
        enemies_in_attack_range = self.scan_for_enemies(self.attack_range)
        if enemies_in_attack_range:
            enemy = random.choice(enemies_in_attack_range)
            self.attack(enemy)
        else:
            self.move()

    def die(self):
        self.type = 'dead'
        self.model.schedule.remove(self)

    def attack(self, enemy):
        enemy.hp -= self.attack_damage
        if enemy.hp <= 0:
            enemy.die()

    # ostateczny wektor prędkości otrzymujemy normalizując wektor prędkości z metody calculate_velocity_vector()
    # i mnożąc go przez szybkość
    # danego typu agenta (skalarną) parametryzowaną w pliku konfiguracyjnym
    def move(self):
        velocity_vector = self.calculate_velocity_vector()
        normalised_velocity_vector = velocity_vector / np.linalg.norm(velocity_vector)
        self.velocity = normalised_velocity_vector * self.movement_speed
        end_point = self.pos + self.velocity
        self.model.space.move_agent(self, end_point)

    def calculate_velocity_vector(self):
        visible_enemies = self.scan_for_enemies(self.ENEMY_SCANNING_RADIUS)
        visible_allies = self.scan_for_allies()

        # wektor prędkości przed normalizacją - kombinacja liniowa wektorów z poszczególnych reguł o współczynnikach
        # równych ich wagom (parametryzowanych w pliku konfiguracyjnym)
        velocity_vector = (self.coherence_vector(visible_allies) * self.COHERENCE_FACTOR +
                           self.match_vector(visible_allies) * self.MATCH_FACTOR +
                           self.separate_vector(visible_allies) * self.SEPARATION_FACTOR +
                           self.coherence_vector(visible_enemies) * self.ENEMY_POSITION_FACTOR)

        return velocity_vector

    def scan_for_allies(self):
        warriors_in_flocking_radius = self.model.space.get_neighbors(self.pos, self.FLOCKING_RADIUS, False)
        allies_in_range = []
        for warrior in warriors_in_flocking_radius:
            if warrior.type == self.type:
                allies_in_range.append(warrior)
        return allies_in_range

    def scan_for_enemies(self, given_range):
        warriors_in_range = self.model.space.get_neighbors(self.pos, given_range, False)
        enemies_in_range = []
        for warrior in warriors_in_range:
            if warrior.type != self.type and warrior.type != 'dead':
                enemies_in_range.append(warrior)
        return enemies_in_range

    # zwraca wektor od agenta do środka danej grupy agentów
    def coherence_vector(self, group_in_radius):
        vector = np.zeros(2)
        if group_in_radius:
            for warrior in group_in_radius:
                vector += self.model.space.get_heading(self.pos, warrior.pos)
            vector /= len(group_in_radius)
        return vector

    def match_vector(self, visible_allies):
        vector = np.zeros(2)
        if visible_allies:
            for ally in visible_allies:
                vector += ally.velocity
            vector /= len(visible_allies)
        return vector

    # wektor przeciwny do położeń agentów w przestrzeni "osobistej" tego agenta
    def separate_vector(self, visible_allies):
        vector = np.zeros(2)
        for ally in visible_allies:
            if self.model.space.get_distance(self.pos, ally.pos) < self.SEPARATION_DISTANCE:
                vector -= self.model.space.get_heading(self.pos, ally.pos)
        return vector

class RedWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'red'
        self.attack_damage = 2
        self.attack_range = 2
        self.movement_speed = model.RED_MOVEMENT_SPEED

class BlueWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'blue'
        self.attack_damage = 2
        self.attack_range = 2
        self.movement_speed = model.BLUE_MOVEMENT_SPEED
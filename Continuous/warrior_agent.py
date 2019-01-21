import mesa.agent
import functools
import numpy as np
import random

import simulation_parameters

class WarriorAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.morale = 100.0
        self.has_killed_recently = False
        self.damage_inflicted_recently = 0.0
        self.velocity = np.zeros(2)
        # recently = in the last turn
        self.damage_received_recently = 0.0
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
        if enemy.receive_damage(self.attack_damage):
            self.has_killed_recently = True
        self.damage_inflicted_recently = self.attack_damage

    # returns if the damage inflicted was a killing blow
    def receive_damage(self, damage):
        self.hp -= damage
        self.damage_received_recently += damage

        if self.hp <= 0:
            self.die()
            return True
        return False

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

    def calculate_own_morale_modifier(self):
        morale_modifier = self.damage_received_morale_modifier() + self.kill_morale_modifier() + self.damage_inflicted_morale_modifier()
        return morale_modifier

    def kill_morale_modifier(self):
        return simulation_parameters.kill_morale_modifier(self.has_killed_recently)

    def damage_received_morale_modifier(self):
        return simulation_parameters.damage_received_morale_modifier(self.damage_received_recently, self.initial_hp)

    def damage_inflicted_morale_modifier(self):
        return simulation_parameters.damage_inflicted_morale_modifier(self.damage_inflicted_recently)

    def update_morale(self, new_morale):
        self.clear_recent_event_trackers()
        self.morale = new_morale
        if self.morale <= 20:
            self.flee()
        self.adjust_attack_damage()

    def flee(self):
        print("Uciekam!")
        self.die()

    def adjust_attack_damage(self):
        self.attack_damage = self.initial_attack_damage * self.morale/100

    def clear_recent_event_trackers(self):
        self.damage_received_recently = 0.0
        self.damage_inflicted_recently = 0.0
        self.has_killed_recently = False

    def get_average_morale_of_allies_in_flocking_radius(self):
        morale = [ally.get_morale() for ally in self.scan_for_allies()]
        if not morale:
            return 0
        return sum(morale)/len(morale)

    def calculate_new_morale(self, average_morale_of_allies) -> float:
        new_morale = (average_morale_of_allies * simulation_parameters.ALLIES_MORALE_WEIGHT) + \
                     (self.calculate_own_morale_modifier() + self.morale) * \
                     (1 - simulation_parameters.ALLIES_MORALE_WEIGHT)
        return new_morale

    def get_morale(self):
        return self.morale

class RedWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'red'
        self.initial_hp = 10.0
        self.hp = 10.0
        self.attack_damage = 2.0
        self.initial_attack_damage = 2.0
        self.attack_range = 2.0
        self.movement_speed = model.RED_MOVEMENT_SPEED

class BlueWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'blue'
        self.attack_range = 2.0
        self.movement_speed = model.BLUE_MOVEMENT_SPEED

class BlueCommonWarrior(BlueWarrior):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hp = 10.0
        self.initial_hp = 10.0
        self.attack_damage = 2.0
        self.initial_attack_damage = 2.0

class BlueEliteWarrior(BlueWarrior):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.morale = 140
        self.hp = 15.0
        self.initial_hp = 15.0
        self.attack_damage = 2.5
        self.initial_attack_damage = 2.5
# server.py
from mesa.visualization.ModularVisualization import ModularServer
from battle_model import BattleModel
from ContinuousWorld import ContinuousWorld
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "w": 1,
                 "h": 1}

    if agent.type == 'red':
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif agent.type == 'blue':
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
    return portrayal

red_agents_col = UserSettableParameter('slider', "Number of red agents columns", 5, 1, 12, 1)
red_agents_row = UserSettableParameter('slider', "Number of red agents rows", 15, 1, 24, 1)
blue_agents_col = UserSettableParameter('slider', "Number of blue agents columns", 5, 1, 12, 1)
blue_agents_row = UserSettableParameter('slider', "Number of blue agents rows", 15, 1, 24, 1)
red_agents_movement = UserSettableParameter('slider', "Red agent movement speed", 0.1, 0.01, 0.3, 0.01)
blue_agents_movement = UserSettableParameter('slider', "Blue agent movement speed", 0.1, 0.01, 0.3, 0.01)
coherence_factor = UserSettableParameter('slider', "Coherence factor", 0.025, 0.001, 0.1, 0.001)
separation_factor = UserSettableParameter('slider', "Separation factor", 0.2, 0.01, 0.5, 0.01)
match_factor = UserSettableParameter('slider', "Match factor", 0.05, 0.01, 0.1, 0.01)
enemy_position_factor = UserSettableParameter('slider', "Enemy position factor", 0.03, 0.01, 0.05, 0.01)
vision_range = UserSettableParameter('slider', "Vision range", 50, 20, 100, 1)
flocking_radius = UserSettableParameter('slider', "Flocking range", 5, 1, 10, 0.5)
separation_distance = UserSettableParameter('slider', "Separation distance", 1, 0.5, 2, 0.1)


canvas = ContinuousWorld(agent_portrayal, 30, 30, 750, 750)

server = ModularServer(BattleModel,
                       [canvas],
                       "Warrior Model",
                       {"red_col": red_agents_col, "red_row": red_agents_row,
					    "blue_col": blue_agents_col, "blue_row": blue_agents_row,
						"red_movement": red_agents_movement, "blue_movement": blue_agents_movement,
						"coherence_factor": coherence_factor, "separation_factor": separation_factor,
						"match_factor": match_factor, "enemy_position_factor": enemy_position_factor,
						"vision_range": vision_range, "flocking_radius": flocking_radius,
						"separation_distance": separation_distance,
						"width": 30.0, "height": 30.0})

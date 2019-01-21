# server.py
from mesa.visualization.ModularVisualization import ModularServer
from battle_model import BattleModel
from ContinuousWorld import ContinuousWorld
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "w": 1,
                 "h": 1,
                 "r": 1}

    if agent.type == 'red':
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif agent.type == 'blue':
        if agent.elite == False:
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
        else:
            portrayal["Shape"] = "circle"
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
    
    portrayal["Type"] = agent.type;
    portrayal["Elite"] = agent.elite;
    return portrayal

red_agents_col = UserSettableParameter('slider', "Number of red agents columns", 3, 1, 7, 1)
red_agents_row = UserSettableParameter('slider', "Number of red agents rows", 5, 1, 7, 1)
red_agents_squad = UserSettableParameter('slider', "Number of red agents squad", 5, 1, 5, 1)
red_agents_movement = UserSettableParameter('slider', "Red agent movement speed", 0.1, 0.01, 0.3, 0.01)
blue_agents_col = UserSettableParameter('slider', "Number of blue agents columns", 3, 1, 7, 1)
blue_agents_row = UserSettableParameter('slider', "Number of blue agents rows", 5, 1, 7, 1)
blue_agents_squad = UserSettableParameter('slider', "Number of blue agents squad", 5, 1, 5, 1)
blue_agents_elite_squad = UserSettableParameter('slider', "Number of blue agents elite squad", 1, 0, 5, 1)
blue_agents_movement = UserSettableParameter('slider', "Blue agent movement speed", 0.1, 0.01, 0.3, 0.01)


canvas = ContinuousWorld(agent_portrayal, 70, 70, 750, 750)

server = ModularServer(BattleModel,
                       [canvas],
                       "Warrior Model",
                       {"red_col": red_agents_col, "red_row": red_agents_row, "red_squad": red_agents_squad,
                        "blue_col": blue_agents_col, "blue_row": blue_agents_row, "blue_squad": blue_agents_squad,
                        "blue_agents_elite_squad": blue_agents_elite_squad, 
                        "red_movement": red_agents_movement, "blue_movement": blue_agents_movement,
                        "width": 70.0, "height": 70.0})

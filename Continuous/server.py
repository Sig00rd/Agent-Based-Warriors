# server.py
from mesa.visualization.ModularVisualization import ModularServer
from battle_model import BattleModel
from ContinuousWorld import ContinuousWorld


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


canvas = ContinuousWorld(agent_portrayal, 30, 30, 750, 750)

server = ModularServer(BattleModel,
                       [canvas],
                       "Warrior Model",
                       {"width": 30.0, "height": 30.0})

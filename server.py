# server.py
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import BattleModel
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.type == 'red':
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif agent.type == 'blue':
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(BattleModel,
                       [grid],
                       "Warrior Model",
                       {"width": 10, "height": 10})

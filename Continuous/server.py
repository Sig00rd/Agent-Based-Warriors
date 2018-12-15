# server.py
from mesa.visualization.ModularVisualization import ModularServer
from model import BattleModel
from ContinuousWorld import ContinuousWorld
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import VisualizationElement

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
		
canvas = ContinuousWorld(agent_portrayal,10,10,500,500)

server = ModularServer(BattleModel,
                       [canvas],
                       "Warrior Model",
                       {"width": 10, "height": 10})
					  
from mesa.visualization.ModularVisualization import VisualizationElement
import simplejson as json

class ContinuousWorld(VisualizationElement):
	package_includes = []
	local_includes = ["ContinuousWorld.js"]

	def __init__(self, portrayal_method, world_width, world_height, canvas_width, canvas_height):
		self.portrayal_method = portrayal_method
		self.world_width = world_width
		self.world_height = world_height
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height
		new_element = "new ContinuousWorld({}, {}, {}, {})"
		new_element = new_element.format(self.world_width, self.world_height, self.canvas_width, self.canvas_height)
		self.js_code = "elements.push(" + new_element + ");"
		
	def render(self, model):
		grid_state = []
		grid_state.append([])
		max_layer = 0;
		for agent in model.schedule.agents:
			portrayal = self.portrayal_method(agent)
			if portrayal:
				while portrayal["Layer"] > max_layer:
					grid_state.append([])
					max_layer += 1
				portrayal["x"] = agent.pos[0]
				portrayal["y"] = agent.pos[1]
				grid_state[portrayal["Layer"]].append(portrayal)
		return grid_state
class Agent:

	def __init__(self, width=None, height=None):
		self.width = 0
		self.height = 0
		self.possible_actions = ["moveLeft", "moveRight", "moveForward", "moveBackward"]
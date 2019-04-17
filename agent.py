class Agent:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.coord=(self.x,self.y)
		self.abstract_actions = ["moveLeft", "moveRight", "moveForward", "moveBackward"]
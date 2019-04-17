import numpy as np
import matplotlib.pyplot as plt

class Environment:

	def __init__(self, grid_min_coord, grid_max_coord, agent_coord, goal_coord):
		self.grid_min_coord = grid_min_coord
		self.grid_max_coord = grid_max_coord
		self.agent_coord = agent_coord
		self.goal_coord = goal_coord
		self.obstacles = []

	def add_obstacle(self, obj_bottom_left, obj_top_right):
		self.obstacles.append((obj_bottom_left, obj_top_right))


	def _state_in_obstacle(self, state, obstacle):

		obstacle_min_coord = obstacle[0]
		obstacle_max_coord = obstacle[1]

		if state[0] <= obstacle_max_coord[0] and state[1] <= obstacle_max_coord[1] and state[0] >= obstacle_min_coord[0] and state[1] >= obstacle_min_coord[1]:
			return True
		else:
			return False

	def is_valid_waypoint(self,coor):
		if coor[0] >= self.grid_min_coord[0] and coor[0] <= self.grid_max_coord[0] and coor[1] >= self.grid_min_coord[1] and coor[1] <= self.grid_max_coord[1]:

			for obstacle in self.obstacles:
				if self._state_in_obstacle(coor, obstacle):
					return False

			return True
		else:
			return False

	def is_goal_state(self, coor):
		if coor[0] == self.goal_coord[0] and coor[1] == self.goal_coord[1]:
			return True
		else:
			return False


	def visualise(self):

		mat = np.zeros(( (self.grid_max_coord[1])+1, (self.grid_max_coord[0])+1 ))
		mat[self.agent_coord[1], self.agent_coord[0]] = 1
		mat[self.goal_coord[1], self.goal_coord[0]] = 1

		for obstacle in self.obstacles:
			print(obstacle)
			x_list = [x for x in range(obstacle[0][0],obstacle[1][0]+1)]
			y_list = [y for y in range(obstacle[0][1],obstacle[1][1]+1)]
			for x in x_list:
				for y in y_list:
					mat[y,x] = 1

		plt.matshow(mat)
		plt.show()


def runner():

	grid_min_coord_x = int(input("enter bottom left x coordinate of grid: "))
	grid_min_coord_y = int(input("enter bottom left y coordinate of grid: "))
	grid_max_coord_x = int(input("enter top right x coordinate of grid: "))
	grid_max_coord_y = int(input("enter top right y coordinate of grid: "))	
		
	agent_coord_x = int(input("enter initial x coordinate of agent: "))
	agent_coord_y = int(input("enter initial y coordinate of agent: "))

	goal_coord_x = int(input("enter x coordinate of goal: "))
	goal_coord_y = int(input("enter y coordinate of goal: "))

	Env = Environment((grid_min_coord_x, grid_min_coord_y), (grid_max_coord_x,grid_max_coord_y), (agent_coord_x,agent_coord_y), (goal_coord_x,goal_coord_y))

	flag = raw_input("do you want to enter any obstacles (Y/N)? ")
	
	while flag == "Y":
		
		bottom_left_coord_x = int(input("\t enter bottom left x coordinate: "))
		bottom_left_coord_y = int(input("\t enter bottom left y coordinate: "))
		top_right_coord_x = int(input("\t enter top right x coordinate: "))
		top_right_coord_y = int(input("\t enter top right y coordinate: "))
		
		Env.add_obstacle((bottom_left_coord_x,bottom_left_coord_y), (top_right_coord_x,top_right_coord_y))

		flag = raw_input("do you want to enter more obstacles (Y/N)? ")

	Env.visualise()

#runner()


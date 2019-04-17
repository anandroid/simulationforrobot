import heapq
from environment import Environment
from agent import Agent
import time
import math
import matplotlib.pyplot as plt
import numpy as np

class WaypointPlanner:

	def __init__(self, environment, agent):
		self.env = environment
		self.agent = agent

	def _state_to_key(self, state):
		return "("+str(state[0])+","+str(state[1])+")"

	def _manhattan_distance(self, state1, state2):
		return ( abs(state1.x-state2.x) + abs(state1.y-state2.y) )

	def _euclidean_distance(self, state1, state2):
	    return math.sqrt((state1[0]-state2[0])**2 + (state1[1]-state2[1])**2)

	def _state_in_obstacle(self, state, obstacle):

		obstacle_min_coord = obstacle[0]
		obstacle_max_coord = obstacle[1]

		if state[0] <= obstacle_max_coord[0] and state[1] <= obstacle_max_coord[1] and state[0] >= obstacle_min_coord[0] and state[1] >= obstacle_min_coord[1]:
			return True
		else:
			return False

	def _get_successor(self, current_state, action):

		next_state = None

		if action == "moveLeft": next_state = (current_state[0]-1, current_state[1])
		elif action == "moveRight": next_state = (current_state[0]+1, current_state[1])
		elif action == "moveForward": next_state = (current_state[0], current_state[1]+1)
		elif action == "moveBackward": next_state = (current_state[0], current_state[1]-1)

		if next_state[0] < self.env.grid_min_coord[0] or next_state[0] > self.env.grid_max_coord[0]: return (None, -1)
		if next_state[1] < self.env.grid_min_coord[1] or next_state[1] > self.env.grid_max_coord[1]: return (None, -1)

		for obstacle in self.env.obstacles:
			if self._state_in_obstacle(next_state, obstacle): return (None, -1)
			
		return (next_state, 1)


	def plan(self):
		
		init_state = self.env.agent_coord
		goal_state = self.env.goal_coord

		possible_actions = self.agent.abstract_actions
		state_list = []

		priority_queue = [(0, init_state)]
		heapq.heapify(priority_queue)
	    
		parsed_states = {}
		parsed_states[self._state_to_key(init_state)] = 1

		trace = {}
		trace[self._state_to_key(init_state)] = None

        #To-Do we need to get the init state based on the initial triangulation calculation
		current_state = init_state
		prev_state = None

		while(len(priority_queue)>0):

			print("----- state loop -----")
			(cost, current_state) = heapq.heappop(priority_queue) 
	        
			if current_state[0]==goal_state[0] and current_state[1]==goal_state[1]:
				break

			for action in possible_actions:
				print(current_state, action)
				(nextstate, cost) = self._get_successor(current_state, action)
				print(nextstate, cost)
				if cost != -1 and self._state_to_key(nextstate) not in parsed_states:
					cost = cost + self._euclidean_distance(nextstate, goal_state)
					if prev_state and prev_state[0]-nextstate[0] != 0 and prev_state[1]-nextstate[1] != 0: cost += 1
					parsed_states[self._state_to_key(nextstate)] = 1
					heapq.heappush(priority_queue, (cost, nextstate))
					trace[self._state_to_key(nextstate)] = (current_state, action)

			prev_state = current_state

		if current_state[0]==goal_state[0] and current_state[1]==goal_state[1]:
			print("solved")
			while(trace[self._state_to_key(current_state)] != None):
				(parent_state, action) = trace[self._state_to_key(current_state)]
				state_list.append(parent_state)
				current_state = parent_state
		else:
			print("unsolved")

		state_list.reverse()
		state_list.append(goal_state)

		return state_list

	def visualise(self, state_list):

		mat = np.zeros(( (self.env.grid_max_coord[1])+1, (self.env.grid_max_coord[0])+1 ))

		for obstacle in self.env.obstacles:
			print(obstacle)
			x_list = [x for x in range(obstacle[0][0],obstacle[1][0]+1)]
			y_list = [y for y in range(obstacle[0][1],obstacle[1][1]+1)]
			for x in x_list:
				for y in y_list:
					mat[y,x] = 1

		for state in state_list:
			mat[state[1],state[0]] = 0.5

		mat[self.env.agent_coord[1], self.env.agent_coord[0]] = 2
		mat[self.env.goal_coord[1], self.env.goal_coord[0]] = 2

		plt.matshow(mat)
		plt.show()

def runner():

	env = Environment((0,0), (100,50), (1,1), (80,30))
	agent = Agent()

	env.add_obstacle((25,10),(75,20))
	env.add_obstacle((25,35), (75,45))

	wp = WaypointPlanner(env, agent)
	plan = wp.plan()

	print(plan)

	wp.visualise(plan)

#runner()

from environment import Environment
from ble import BLE 
from agent import Agent
from trajectory import Trajectory
from waypoint_planner import WaypointPlanner
from trajectory import Trajectory

grid_min_coord_x = int(input("enter bottom left x coordinate of grid: "))
grid_min_coord_y = int(input("enter bottom left y coordinate of grid: "))
grid_max_coord_x = int(input("enter top right x coordinate of grid: "))
grid_max_coord_y = int(input("enter top right y coordinate of grid: "))	
	
agent_coord_x = int(input("enter initial x coordinate of agent: "))
agent_coord_y = int(input("enter initial y coordinate of agent: "))

goal_coord_x = int(input("enter x coordinate of goal: "))
goal_coord_y = int(input("enter y coordinate of goal: "))

Env = Environment((grid_min_coord_x, grid_min_coord_y), (grid_max_coord_x,grid_max_coord_y), (agent_coord_x,agent_coord_y), (goal_coord_x,goal_coord_y))

flag = input("do you want to enter any obstacles (Y/N)? ")

while flag == "Y":
	
	bottom_left_coord_x = int(input("\t enter bottom left x coordinate: "))
	bottom_left_coord_y = int(input("\t enter bottom left y coordinate: "))
	top_right_coord_x = int(input("\t enter top right x coordinate: "))
	top_right_coord_y = int(input("\t enter top right y coordinate: "))
	
	Env.add_obstacle((bottom_left_coord_x,bottom_left_coord_y), (top_right_coord_x,top_right_coord_y))

	flag = input("do you want to enter more obstacles (Y/N)? ")

agent = Agent()

ble1 = BLE(4, -73, (0,0))
ble2 = BLE(4, -73, (100,0))
ble3 = BLE(4, -73, (50,50))

wp = WaypointPlanner(env, agent)
plan = wp.plan()

print(plan)

wp.visualise(plan)



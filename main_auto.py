from environment import Environment
from ble import BLE
from agent import Agent
from trajectory import Trajectory
from waypoint_planner import WaypointPlanner
from trajectory import Trajectory
from pomdp_waypoint_planner import PomdpWaypointPlanner
import numpy as np
import random
import math
import scipy.stats
from all_Ble import A_BLE
import all_Ble as blemodule
import tupleutilities as TU


SIZE_FACTOR_OF_WAYPOINT = 2
BELIEF_FOR_ACTION_SUCCESSFUL = 0.8
BELIEF_FOR_ADJACENT_ACTION = 0.4
BELIEF_FOR_OTHER_ACTION = 0.2

BELIEF_FACTOR=0.1
EPOCH_FACTOR=2


grid_min_coord_x = 0
grid_min_coord_y = 0
grid_max_coord_x = 10
grid_max_coord_y = 10

initial_agent_coord_x = 1
initial_agent_coord_y = 1

goal_coord_x = 9
goal_coord_y = 5

env = Environment((grid_min_coord_x, grid_min_coord_y), (grid_max_coord_x, grid_max_coord_y),
                  (initial_agent_coord_x, initial_agent_coord_y), (goal_coord_x, goal_coord_y))

flag = "Y"

obsacles=[((5,5),(6,6)),((8,3),(9,4))]

for obsacle in obsacles:

    bottom_left_coord_x = obsacle[0][0]
    bottom_left_coord_y = obsacle[0][1]
    top_right_coord_x = obsacle[1][0]
    top_right_coord_y = obsacle[1][1]

    env.add_obstacle((bottom_left_coord_x, bottom_left_coord_y), (top_right_coord_x, top_right_coord_y))


agent = Agent(initial_agent_coord_x,initial_agent_coord_y)



'''

wp = PomdpWaypointPlanner(env, agent)
plan,actions = wp.plan()

agent.coord=(4,0)
wp = PomdpWaypointPlanner(env,agent)
new_plan,actions=wp.plan()

plan=plan+new_plan


print(plan)
print ("plan size "+str(len(plan)))
print (actions)
print ("action size "+str(len(actions)))

wp.visualise(plan)
'''

def execute_plan():

    bles = []

    ble1 = A_BLE(4, -73, (0, 0))
    ble2 = A_BLE(4, -73, (0, 10))
    ble3 = A_BLE(4, -73, (10, 0))
    ble4 = A_BLE(4, -73, (10, 10))
    ble5 = A_BLE(4, -73, (5, 5))
    ble6 = A_BLE(4, -73, (2, 8))
    ble7 = A_BLE(4, -73, (8, 2))
    ble8 = A_BLE(4, -73, (4, 6))


    bles.append(ble1)
    bles.append(ble2)
    bles.append(ble3)
    bles.append(ble4)
    bles.append(ble5)
    bles.append(ble6)
    bles.append(ble7)
    bles.append(ble8)


    trace = []


    waypoints = blemodule.fill_the_way_points(bles)
    beliefs = blemodule.fill_beliefs_equally(waypoints)
    real_point = agent.coord
    wp = PomdpWaypointPlanner(env, agent)




    reached = False

    proposed_plan=[]
    proposed_actions=[]

    replan = True


    while reached==False:

        if replan == True:
          wp = PomdpWaypointPlanner(env, agent)
          proposed_plan, proposed_actions = wp.plan()
          #print(proposed_plan.pop(0))
         # break


        rssi_values = {}

        for ble in bles:
            rssi_values[ble.ID] = ble.coord_to_rssi(real_point)
            #print (rssi_values[ble.ID])


        waypoint_name = ""

        max_value = -10000

        for waypoint in waypoints:
            value = 0

            for ble in bles:
               value+=math.log(scipy.stats.norm(waypoint.means[ble.ID], waypoint.variances[ble.ID]).pdf(rssi_values[ble.ID]))

            value+=math.log(beliefs[waypoint.W])


            if value>max_value :
                waypoint_name = waypoint.W
                max_value = value

            #print("Waypoint :" + waypoint.W + "Value " + str(value))

        #print("Predicted  : "+waypoint_name)

        beliefs[waypoint_name]+=BELIEF_FOR_ACTION_SUCCESSFUL

        if len(proposed_actions) == 0:
            print("No actions found")
            agent.coord = predicted_tuple
            replan = True
            continue

        #action = possible_actions[random.randint(0,len(possible_actions)-1)]
        action = proposed_actions.pop(0)


        proposed_tuple = proposed_plan.pop(0)

        waypoint_tuple_str = waypoint_name.split("_")
        waypoint_tuple = (int(waypoint_tuple_str[0]),int(waypoint_tuple_str[1]))
        predicted_tuple = waypoint_tuple

        trace.append(real_point)

        if env.is_goal_state(predicted_tuple):
            print("Goal reached")
            reached = True
            continue

        if TU.cmp(predicted_tuple,proposed_tuple)!=0:
            #note real point is not moved for sake of simulation, we make plan assuming robot is at predicted point
            agent.coord = predicted_tuple
            replan = True
            print("-------")
            print("proposed :")
            print(proposed_tuple)
            print("predicted :")
            print(predicted_tuple)
            print("real :")
            print(real_point)
            continue
            #you can take the real action as it is believed you are on correct path
        else:
            replan = False


        underministic_action = random.randint(50,100)

        tuples = TU.getTuplesInPriorityForAction(waypoint_tuple,action)
        for i in range(len(tuples)):
            tuple = tuples[i]
            if i==0:
                if env.is_valid_waypoint(tuple):
                  beliefs[TU.getStringFromTuple(tuple)]+=BELIEF_FOR_ACTION_SUCCESSFUL
                else:
                  beliefs[TU.getStringFromTuple(tuple)] += BELIEF_FOR_ACTION_SUCCESSFUL


            if i>0 and i<6:
                slot_for_i = ((6+(i*3)),(6+(i+1)*3))
                if env.is_valid_waypoint(tuple):
                  beliefs[TU.getStringFromTuple(tuple)]+=BELIEF_FOR_ADJACENT_ACTION
                else:
                   beliefs[TU.getStringFromTuple(waypoint_tuple)] += BELIEF_FOR_ADJACENT_ACTION


            if i==6 or i==7:
                if i==6:
                    slot_for_i=(4,6)
                if i==7:
                    slot_for_i=(2,4)
                if env.is_valid_waypoint(tuple):
                   beliefs[TU.getStringFromTuple(tuple)] += BELIEF_FOR_OTHER_ACTION
                else:
                    beliefs[TU.getStringFromTuple(waypoint_tuple)] += BELIEF_FOR_OTHER_ACTION

            if i==8:
                slot_for_i=(0,2)
                if env.is_valid_waypoint(tuple):
                   beliefs[TU.getStringFromTuple(tuple)] += BELIEF_FOR_OTHER_ACTION
                else:
                    beliefs[TU.getStringFromTuple(waypoint_tuple)] += BELIEF_FOR_OTHER_ACTION


        tuples = TU.getTuplesInPriorityForAction(real_point, action)
        for i in range(len(tuples)):
                tuple = tuples[i]
                if i == 0:
                    if env.is_valid_waypoint(tuple):
                      if underministic_action > 21:
                        real_point = tuple
                    else:
                        real_point = real_point

                if i > 0 and i < 6:
                    slot_for_i = ((6 + ((i-1) * 3)), (6 + (i) * 3))
                    if env.is_valid_waypoint(tuple):
                        if underministic_action > slot_for_i[0] and underministic_action <= slot_for_i[1]:
                            real_point = tuple
                    else:
                        if underministic_action > slot_for_i[0] and underministic_action <= slot_for_i[1]:
                            real_point = real_point

                if i == 6 or i == 7:
                    if i == 6:
                        slot_for_i = (4, 6)
                    if i == 7:
                        slot_for_i = (2, 4)
                    if env.is_valid_waypoint(tuple):
                        if underministic_action > slot_for_i[0] and underministic_action <= slot_for_i[1]:
                            real_point = tuple
                    else:
                        if underministic_action > slot_for_i[0] and underministic_action <= slot_for_i[1]:
                            real_point = real_point

                if i == 8:
                    slot_for_i = (0, 2)
                    if env.is_valid_waypoint(tuple):
                        if underministic_action > slot_for_i[0] and underministic_action <= slot_for_i[1]:
                            real_point = tuple
                    else:
                        if underministic_action > slot_for_i[0] and underministic_action <= slot_for_i[1]:
                            real_point = real_point
        #print("real point :")
        #print (real_point)


    #print("Action took : "+action+" New point "+str(test_point[0])+"_"+str(test_point[1]));

    print (trace)
    wp.visualise(trace)


execute_plan()




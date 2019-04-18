import numpy as np
import random
import math
import scipy.stats
from agent import Agent


SIZE_FACTOR_OF_WAYPOINT = 1
BELIEF_FOR_ACTION_SUCCESSFUL = 0.8
BELIEF_FOR_ADJACENT_ACTION = 0.4
BELIEF_FOR_OTHER_ACTION = 0.2

class WayPoint:
      def __init__(self,W,means,variances):
          self.W = W
          self.means = means
          self.variances = variances

class A_BLE:

    def __init__(self, N, measured_power, coord):
        self.ID = hex(random.randrange(0, 2 ^ 16))
        self.N = N
        self.measured_power = measured_power
        self.noise_std_dev = random.uniform(0, 4)
        self.coord = coord
        self.waypoints = []

    def _euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)*SIZE_FACTOR_OF_WAYPOINT

    def distance_to_rssi(self, distance):
        rssi = self.measured_power
        if distance > 0:
            rssi = self.measured_power - (math.log(distance, 10) * 10 * self.N)
        else:
            rssi = rssi/5
        return rssi

    def coord_to_rssi(self, coord):
        distance = self._euclidean_distance(self.coord, coord)
        rssi = self.distance_to_rssi(distance)
        rssi -= np.random.normal(0, self.noise_std_dev)
        return rssi

    def coord_to_rssi_without_noise(self, coord):
        distance = self._euclidean_distance(self.coord, coord)
        rssi = self.distance_to_rssi(distance)
        return rssi



def fill_beliefs_equally(waypoints):
     beliefs = {}
     value = 1
     for waypoint in waypoints:
         beliefs[waypoint.W] = value
     return beliefs




def fill_the_way_points(bles):
    waypoints = []
    variance = 4
    for i in range(0,11):
       for j in range(0,11):
          means={}
          variances = {}
          for ble in bles:
             means[ble.ID]= ble.coord_to_rssi_without_noise((i,j))
             variances[ble.ID] = variance
          waypoint = WayPoint(str(i) + "_" + str(j),means,variances)
          waypoints.append(waypoint)
    return waypoints

def is_valid_waypoint(coor):
    if coor[0]>=0 and coor[0]<=10 and coor[1]>=0 and coor[1]<=10:
        return True
    else :
        return False


def runner():

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


    waypoints = fill_the_way_points(bles)
    beliefs = fill_beliefs_equally(waypoints)

    test_point = (8, 5)

    agent = Agent()
    possible_actions = agent.abstract_actions

    for i in range(1,10):

        rssi_values = {}

        for ble in bles:
            rssi_values[ble.ID] = ble.coord_to_rssi(test_point)
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

        print("Predicted  : "+waypoint_name)

        beliefs[waypoint_name]+=BELIEF_FOR_ACTION_SUCCESSFUL

        action = possible_actions[random.randint(0,len(possible_actions)-1)]

        waypoint_tuple_str = waypoint_name.split("_")
        waypoint_tuple = (int(waypoint_tuple_str[0]),int(waypoint_tuple_str[1]))


        if action == "moveLeft":
             if is_valid_waypoint((waypoint_tuple[0]-1,waypoint_tuple[1])):
                 beliefs[str(waypoint_tuple[0]-1)+"_"+str(waypoint_tuple[1])]+=BELIEF_FOR_ACTION_SUCCESSFUL
                 test_point = (test_point[0]-1,test_point[1])
             else:
                 beliefs[waypoint_name]+=BELIEF_FOR_ACTION_SUCCESSFUL

             if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1]-1)):
                 beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1]-1)] += BELIEF_FOR_ADJACENT_ACTION
             else:
                 beliefs[waypoint_name]+=BELIEF_FOR_ADJACENT_ACTION

             if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1] + 1)):
                 beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_ADJACENT_ACTION
             else:
                 beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

             if is_valid_waypoint((waypoint_tuple[0], waypoint_tuple[1] - 1)):
                 beliefs[str(waypoint_tuple[0]) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_OTHER_ACTION
             else:
                 beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

             if is_valid_waypoint((waypoint_tuple[0], waypoint_tuple[1] + 1)):
                 beliefs[str(waypoint_tuple[0]) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_OTHER_ACTION
             else:
                 beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

             if is_valid_waypoint((waypoint_tuple[0]+1, waypoint_tuple[1] - 1)):
                 beliefs[str(waypoint_tuple[0]+1) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_ADJACENT_ACTION
             else:
                 beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

             if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1])):
                 beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1])] += BELIEF_FOR_ADJACENT_ACTION
             else:
                 beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

             if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1] + 1)):
                 beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_ADJACENT_ACTION
             else:
                 beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION



        if action == "moveRight":
            if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1])):
                beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1])] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1] - 1)):
                beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1] + 1)):
                beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0], waypoint_tuple[1] - 1)):
                beliefs[str(waypoint_tuple[0]) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_OTHER_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0], waypoint_tuple[1] + 1)):
                beliefs[str(waypoint_tuple[0]) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_OTHER_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1] - 1)):
                beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1])):
                beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1])] += BELIEF_FOR_ACTION_SUCCESSFUL
                test_point = (test_point[0] + 1, test_point[1])
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ACTION_SUCCESSFUL

            if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1] + 1)):
                beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

        if action == "moveForward":
            if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1])):
                beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1])] += BELIEF_FOR_OTHER_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1] - 1)):
                beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1] + 1)):
                beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0], waypoint_tuple[1] - 1)):
                beliefs[str(waypoint_tuple[0]) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0], waypoint_tuple[1] + 1)):
                beliefs[str(waypoint_tuple[0]) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_ACTION_SUCCESSFUL
                test_point = (test_point[0], test_point[1]+1)
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ACTION_SUCCESSFUL

            if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1] - 1)):
                beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1])):
                beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1])] += BELIEF_FOR_OTHER_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1] + 1)):
                beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

        if action == "moveBackward":
            if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1])):
                beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1])] += BELIEF_FOR_OTHER_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1] - 1)):
                beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] - 1, waypoint_tuple[1] + 1)):
                beliefs[str(waypoint_tuple[0] - 1) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0], waypoint_tuple[1] - 1)):
                beliefs[str(waypoint_tuple[0]) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_ACTION_SUCCESSFUL
                test_point = (test_point[0],test_point[1]-1)
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ACTION_SUCCESSFUL

            if is_valid_waypoint((waypoint_tuple[0], waypoint_tuple[1] + 1)):
                beliefs[str(waypoint_tuple[0]) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1] - 1)):
                beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1] - 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1])):
                beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1])] += BELIEF_FOR_OTHER_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

            if is_valid_waypoint((waypoint_tuple[0] + 1, waypoint_tuple[1] + 1)):
                beliefs[str(waypoint_tuple[0] + 1) + "_" + str(waypoint_tuple[1] + 1)] += BELIEF_FOR_ADJACENT_ACTION
            else:
                beliefs[waypoint_name] += BELIEF_FOR_ADJACENT_ACTION

        print("Action took : "+action+" New point "+str(test_point[0])+"_"+str(test_point[1]));

    print(beliefs)












#runner()



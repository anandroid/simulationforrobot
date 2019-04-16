class Trajectory:

	def __init__(self):

		self.turn_actions = ["turnCW", "turnCCW"]
		self.move_actions = ["moveF"]

		self.moveFoward = self.move_actions[0]
		self.turnClockWise = self.turn_actions[0]
		self.turnAntiClockWise = self.turn_actions[1]


	def _euclidean_distance(self, state1, state2):
    	 return math.sqrt((state1[0]-state2[0])**2 + (state1[1]-state2[1])**2)

	def _calculate_correction_angle(self, current_point,to_point):
		 distance_error_offset = 1/self._euclidean_distance(current_point, to_point)
		 angle_correction = math.degrees(math.atan(distance_error_offset))
		 return angle_correction

	def _map_to_action(self):
		pass

	def check_correction(self, current_point,to_point,theta):

		 axis_angle = self._calculate_correction_angle(current_point,to_point)
		 difference = axis_angle-theta

		 #choose between close wise or anticlockwise

		 if difference > 180:
			 ccw_angle_to_rotate = abs(difference-180)
			 return self.turnAntiClockWise+ " "+ccw_angle_to_rotate

		 if difference<0 and difference<-180:
			 ccw_angle_to_rotate = abs(difference)
			 return self.turnAntiClockWise+ " "+ccw_angle_to_rotate

		 if difference<0 and difference>-180:
			 cw_angle_to_rotate = 90+axis_angle
			 return self.turnClockWise+ " "+cw_angle_to_rotate

		 if difference > 0 and difference < 180:
			 cw_angle_to_rotate = difference
			 return self.turnClockWise + " " + cw_angle_to_rotate


		 return self.turnClockWise+ " "+difference


	def plan(self, from_point, to_point, theta):

		# values of theta
		# 	0 - facing north
		# 	90 - facing east
		# 	180 - facing south
		# 	270 - facing west


		actions = []

		reached = False

		current_point = from_point


		while reached == False:

			delta_x = self.to_point[0] - self.current_point[0]
			delta_y = self.to_point[1] - self.current_point[1]

			actions.append(self.check_correction(current_point,to_point,theta))

			actions.append(self.moveFoward)

			# case for moving towards north
			if delta_x == 0 and delta_y > 0:
				current_point[1] = current_point[1]+1


			# case for moving towards south
			elif delta_x == 0 and delta_y < 0:
				current_point[1] = current_point[1] - 1


			# case for moving towards east
			elif delta_y == 0 and delta_x > 0:
				current_point[0] = current_point[0] + 1

			# case for moving towards west
			elif delta_y == 0 and delta_x < 0:
				current_point[0] = current_point[0] - 1



			if (current_point[0] == to_point[0]) and (current_point[1] == to_point[1]):
				reached = True



		return actions






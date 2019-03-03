## SAOF-Sim: The Simple Autonomous Order Fulfillment Simulator 
## Author: Kyle E. C. Booth
## Email: kbooth@mie.utoronto.ca
## File description: Specify allocation logic. Define our own allocator/scheduler here (with appropriate adjustments in simulator.py). 

import numpy as np
from allocator_params import *
import pandas as pd

def allocateRandom(master_queue, available_robots, time): 
	robot_index = 0
	assigned = 0
	task_tracking = [] 
	assignment = []
	while robot_index < len(available_robots) and assigned < len(master_queue):
		task_index = np.random.random_integers(0, len(master_queue) - 1)
		if (task_index not in task_tracking):
			task_tracking.append(task_index)
			assignment.append([available_robots[robot_index].robot_details["ID"], master_queue[task_index].task_details["ID"]])
			robot_index = robot_index + 1
			assigned = assigned + 1
	return assignment

def allocateNaive(master_queue, available_robots, time):
	assignment_index = 0
	assignment = []
	for i in range(len(master_queue)):
		if assignment_index < len(available_robots):
			assignment.append([available_robots[assignment_index].robot_details["ID"], master_queue[i].task_details["ID"]])
			print("task value: ", master_queue[i].task_value)
		assignment_index = assignment_index + 1
	return assignment	

def allocateWSPT(master_queue, available_robots, distance_matrix):
	#for each task: for each robot: distance between subtasks[0] and robot
	#Pij = divide distance by robot speed
	#Nij = divide task value by Pij
	#sort Nij greatest to least
	#assign to available robots

	assignment = []

	robot_task_table = []
	# NOTE!!!!! FIX BELOW: should be for robot i then task j
	for robot_i in available_robots:
		robot_task_j_ranks = []
		for task_j in master_queue:
			# robot_id = robot_i.robot_details["ID"]
			# task_id = task_j.task_details["ID"]
			
			#distance between robot i and first subtask of task j
			distance = distance_matrix[robot_i.robot_details["location"]][task_j.subtask_locations[0]]
			
			time_taken = distance/robot_i.movement_speed
			task_value = task_j.task_value
			print("time taken: ", time_taken)
			print("task_value: ", task_value)
			rank = task_value / time_taken
			robot_task_j_ranks.append(rank)
		
		robot_task_table.append(robot_task_j_ranks)
	
	robot_task_table = pd.DataFrame(robot_task_table)
	#while tasks still unassigned
	#flatten table
	#sort by sorted(list, key, reverse)
	#use result index at 1 to delete row at index
	#repeat
	print("starting table: ", robot_task_table)

	while not robot_task_table.empty:
		max_rank = 0
		max_task = None
		max_robot = None
		for i in robot_task_table:
			if max(robot_task_table[i]) > max_rank:
				max_robot = robot_task_table[i].idxmax()
				max_task = i
				max_rank = robot_task_table[i][max_robot]
		print("[max robot, max task]: ", [max_robot, max_task])
		assignment.append([available_robots[max_robot].robot_details["ID"], master_queue[max_task].task_details["ID"]])
		
		robot_task_table.drop(max_robot, inplace=True) 
		robot_task_table.drop(max_task, axis=1, inplace=True)
		print("table: ", robot_task_table)
	print(assignment)
	return assignment

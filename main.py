## SAOF-Sim: The Simple Autonomous Order Fulfillment Simulator
## Author: Kyle E. C. Booth
## Email: kbooth@mie.utoronto.ca
## File description: Main function. Loads problem/simulation params and calls simulateFactory(). Outputs makespan.

import numpy as np
import pandas as pd
import pprint as pp
import time
from simulator import *
import sys

if __name__ == "__main__":
	args = sys.argv[1:]
    ## Adjust below parameters for your experiments

	#max_subtasks should <= locations or there will be multiple subtasks per location (which will be completed together anyway)
	problem_parameters = {
        "robot_num": 10,
        "max_subtasks": 10,
        "max_tasks": 60,
        "initial_percentage": 0.3,
        "horizon": 100,
        "max_distance": 100,
        "locations": 100,
        "max_task_value": 10,
    }

	simulation_parameters = {
        "random_seed": 3,
        "rate": 1.5,
        "allocation_method": str(args[0]) if args else "WSPT",
        "min_available_robots": 1,
        "max_wait": 0,
    }
	print(simulation_parameters["allocation_method"])
	makespan = simulateFactory(problem_parameters, simulation_parameters)

	print(
        "\n|===|\n(COMPLETE) Execution Sum Of Job Completion Time: %d \n|===|"
        % (makespan)
    )


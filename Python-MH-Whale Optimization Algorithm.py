############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Course: Metaheuristics
# Lesson: Whale Optimization Algorithm

# Citation: 
# PEREIRA, V. (2018). Project: Metaheuristic-Whale_Optimization_Algorithm, File: Python-MH-Whale Optimization Algorithm.py, GitHub repository: <https://github.com/Valdecy/Metaheuristic-Whale_Optimization_Algorithm>

############################################################################

# Required Libraries
import numpy  as np
import math
import random
import os

# Function
def target_function():
    return

# Function: Initialize Variables
def initial_position(hunting_party = 5, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    position = np.zeros((hunting_party, len(min_values)+1))
    for i in range(0, hunting_party):
        for j in range(0, len(min_values)):
             position[i,j] = random.uniform(min_values[j], max_values[j])
        position[i,-1] = target_function(position[i,0:position.shape[1]-1])
    return position

# Function: Initialize Alpha
def leader_position(dimension = 2, target_function = target_function):
    leader = np.zeros((1, dimension+1))
    for j in range(0, dimension):
        leader[0,j] = 0.0
    leader[0,-1] = target_function(leader[0,0:leader.shape[1]-1])
    return leader

# Function: Updtade Leader by Fitness
def update_leader(position, leader):
    for i in range(0, position.shape[0]):
        if (leader[0,-1] > position[i,-1]):
            for j in range(0, position.shape[1]):
                leader[0,j] = position[i,j]
    return leader

# Function: Updtade Position
def update_position(position, leader, a_linear_component = 2, b_linear_component = 1,  spiral_param = 1, min_values = [-5,-5], max_values = [5,5], target_function = target_function): 
    for i in range(0, position.shape[0]):           
            r1_leader = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            r2_leader = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            a_leader  = 2*a_linear_component*r1_leader - a_linear_component
            c_leader  = 2*r2_leader           
            p         = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)           
            for j in range (0, len(min_values)):
                if (p < 0.5):
                    if (abs(a_leader) >= 1):
                        rand              = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                        rand_leader_index = math.floor(position.shape[0]*rand);
                        x_rand            = position[rand_leader_index, :]
                        distance_x_rand   = abs(c_leader*x_rand[j] - position[i,j]) 
                        position[i,j]     = x_rand[j] - a_leader*distance_x_rand                            
                    elif (abs(a_leader) < 1):
                        distance_leader   = abs(c_leader*leader[0,j] - position[i,j]) 
                        position[i,j]     = leader[0,j] - a_leader*distance_leader                              
                elif (p >= 0.5):      
                    distance_Leader       = abs(leader[0,j] - position[i,j])
                    rand                  = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                    m_param               = (b_linear_component - 1)*rand + 1
                    position[i,j]         = np.clip( (distance_Leader*math.exp(spiral_param*m_param)*math.cos(m_param*2*math.pi) + leader[0,j]), min_values[j],  max_values[j])              
            position[i,-1] = target_function(position[i,0:position.shape[1]-1])           
    return position

# WOA Function
def whale_optimization_algorithm(hunting_party = 5, spiral_param = 1,  min_values = [-5,-5], max_values = [5,5], iterations = 50, target_function = target_function):    
    count    = 0
    position = initial_position(hunting_party = hunting_party, min_values = min_values, max_values = max_values, target_function = target_function)
    leader   = leader_position(dimension = len(min_values), target_function = target_function)
    while (count <= iterations):
        print("Iteration = ", count, " f(x) = ", leader[0,-1])
        a_linear_component =  2 - count*( 2/iterations)
        b_linear_component = -1 + count*(-1/iterations)
        leader             = update_leader(position, leader)
        position           = update_position(position, leader, a_linear_component = a_linear_component, b_linear_component = b_linear_component,  spiral_param = spiral_param, min_values = min_values, max_values = max_values, target_function = target_function)
        count = count + 1 
    print(leader)    
    return leader

######################## Part 1 - Usage ####################################

# Function to be Minimized (Six Hump Camel Back). Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def six_hump_camel_back(variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

woa = whale_optimization_algorithm(hunting_party = 100, spiral_param = 0.5,  min_values = [-5, -5], max_values = [5,5], iterations = 100, target_function = six_hump_camel_back)

# Function to be Minimized (Rosenbrocks Valley). Solution ->  f(x) = 0; xi = 1
def rosenbrocks_valley(variables_values = [0,0]):
    func_value = 0
    last_x = variables_values[0]
    for i in range(1, len(variables_values)):
        func_value = func_value + (100 * math.pow((variables_values[i] - math.pow(last_x, 2)), 2)) + math.pow(1 - last_x, 2)
    return func_value

woa = whale_optimization_algorithm(hunting_party = 100, spiral_param = 0.5,  min_values = [-5,-5], max_values = [5,5], iterations = 200, target_function = rosenbrocks_valley)

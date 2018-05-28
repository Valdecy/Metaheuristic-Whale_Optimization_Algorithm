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
import pandas as pd
import numpy  as np
import math
import random
import os

# Function: Initialize Variables
def initial_position(hunting_party = 5, min_values = [-5,-5], max_values = [5,5]):
    position = pd.DataFrame(np.zeros((hunting_party, len(min_values))))
    position['Fitness'] = 0.0
    for i in range(0, hunting_party):
        for j in range(0, len(min_values)):
             position.iloc[i,j] = random.uniform(min_values[j], max_values[j])
        position.iloc[i,-1] = target_function(position.iloc[i,0:position.shape[1]-1])
    return position

# Function: Initialize Alpha
def leader_position(dimension = 2):
    leader = pd.DataFrame(np.zeros((1, dimension)))
    leader['Fitness'] = 0.0
    for j in range(0, dimension):
        leader.iloc[0,j] = 0.0
    leader.iloc[0,-1] = target_function(leader.iloc[0,0:leader.shape[1]-1])
    return leader

# Function: Updtade Leader by Fitness
def update_leader(position, leader):
    updated_position = position.copy(deep = True)
    for i in range(0, position.shape[0]):
        if (updated_position.iloc[i,-1] < leader.iloc[0,-1]):
            for j in range(0, updated_position.shape[1]):
                leader.iloc[0,j] = updated_position.iloc[i,j]
    return leader

# Function: Updtade Position
def update_position(position, leader, a_linear_component = 2, b_linear_component = 1,  spiral_param = 1, min_values = [-5,-5], max_values = [5,5]):
    updated_position = position.copy(deep = True)
    
    for i in range(0, updated_position.shape[0]):
           
            r1_leader = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            r2_leader = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            a_leader = 2*a_linear_component*r1_leader - a_linear_component
            c_leader = 2*r2_leader
            
            p = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            
            for j in range (0, len(min_values)):
                if (p < 0.5):
                    if (abs(a_leader) >= 1):
                        rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                        rand_leader_index = math.floor(updated_position.shape[0]*rand);
                        x_rand = updated_position.iloc[rand_leader_index, :]
                        distance_x_rand = abs(c_leader*x_rand[j] - updated_position.iloc[i,j]) 
                        updated_position.iloc[i,j] = x_rand[j] - a_leader*distance_x_rand                            
                    elif (abs(a_leader) < 1):
                        distance_leader = abs(c_leader*leader.iloc[0,j] - updated_position.iloc[i,j]) 
                        updated_position.iloc[i,j] = leader.iloc[0,j] - a_leader*distance_leader                              
                elif (p >= 0.5):      
                    distance_Leader = abs(leader.iloc[0,j] - updated_position.iloc[i,j])
                    rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                    m_param = (b_linear_component - 1)*rand + 1
                    updated_position.iloc[i,j] = distance_Leader*math.exp(spiral_param*m_param)*math.cos(m_param*2*math.pi) + leader.iloc[0,j]
            if (updated_position.iloc[i,j] > max_values[j]):
                updated_position.iloc[i,j] = max_values[j]
            elif (updated_position.iloc[i,j] < min_values[j]):
                updated_position.iloc[i,j] = min_values[j]        
        
            updated_position.iloc[i,-1] = target_function(updated_position.iloc[i,0:updated_position.shape[1]-1])
            
    return updated_position

# WOA Function
def whale_optimization_algorithm(hunting_party = 5, spiral_param = 1,  min_values = [-5,-5], max_values = [5,5], iterations = 50):    
    count = 0
    position = initial_position(hunting_party = hunting_party, min_values = min_values, max_values = max_values)
    leader = leader_position(dimension = len(min_values))

    while (count <= iterations):
        
        print("Iteration = ", count, leader.iloc[leader['Fitness'].idxmin(),-1])
        
        a_linear_component =  2 - count*( 2/iterations)
        b_linear_component = -1 + count*(-1/iterations)
                
        leader = update_leader(position, leader)
        position = update_position(position, leader, a_linear_component = a_linear_component, b_linear_component = b_linear_component,  spiral_param = spiral_param, min_values = min_values, max_values = max_values)
        
        count = count + 1 
        
    print(leader.iloc[leader['Fitness'].idxmin(),:].copy(deep = True))    
    return leader.iloc[leader['Fitness'].idxmin(),:].copy(deep = True)

######################## Part 1 - Usage ####################################

# Function to be Minimized. Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def target_function (variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

woa = whale_optimization_algorithm(hunting_party = 5, spiral_param = 2,  min_values = [-5,-5], max_values = [5,5], iterations = 100)

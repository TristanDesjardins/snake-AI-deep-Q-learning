# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 17:18:43 2022

@author: X2029440
"""

import numpy as np 
import matplotlib.pyplot as plt 
import networkx as nx
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon



#class used for game states 
#gives information of one point's position relative to another one 
class Points : 

  
    #rotate n times a list 
    @staticmethod
    def rotate(l, n):
        return l[n:] + l[:n]


    #get position of pt2 relative to pt1
    #return vector with 0s and 1 in the right place
    #[N, NE, E, SE, S, SO, O, NO] #clockwise (S:sud, N:nord, E:est, O:ouest)
    #ex : [0,1,0,0,0,0,0,0] signifie que pt2 est au nord est de pt1 (on suppose que pt1 fait face vers le haut)
    @staticmethod
    def get_relative_position(pt1, pt2) : 

        relative_position = [0 for k in range(8)] 
        diff = (pt2[0] - pt1[0], pt2[1] - pt1[1])

        if diff[0] == 0 and diff[1] < 0 : relative_position[0] = 1 
        elif diff[0] == 0 and diff[1] > 0 : relative_position[4] = 1 
        elif diff[0] > 0 and diff[1] == 0 : relative_position[2] = 1
        elif diff[0] < 0 and diff[1] == 0 : relative_position[6] = 1

        elif diff[0] < 0 and diff[1] < 0 : relative_position[7] = 1
        elif diff[0] > 0 and diff[1] > 0 : relative_position[3] = 1
        elif diff[0] < 0 and diff[1] > 0 : relative_position[5] = 1
        elif diff[0] > 0 and diff[1] < 0 : relative_position[1] = 1

        return relative_position


    @staticmethod  
    #idem get_relative_position() mais on prend en compte la direction vers laquelle pointe pt1
    #direction : direction de pt1 
    # par exemple, si pt2 est à droite de pt1 et que pt1 est dirigé vers la droite, alors pt2 est en fait au nord de pt1 
    #ex : [0,1,0,0,0,0,0,0] signifie que pt2 est au nord est de pt1 (en prenant en compte la direction de pt1)
    def get_relative_position_with_direction(pt1, pt2, direction) : 
        if direction == 'UP' : return Points.rotate(Points.get_relative_position(pt1, pt2),0)
        elif direction == 'RIGHT' : return Points.rotate(Points.get_relative_position(pt1, pt2),2)
        elif direction == 'DOWN' : return Points.rotate(Points.get_relative_position(pt1, pt2),4)
        elif direction == 'LEFT' : return Points.rotate(Points.get_relative_position(pt1, pt2),6)



    #renvoie un vecteur de taille 4  [N,E,S,O]
    #met un 1 à l'endroit ou se trouve pt2 par rapport à pt1 (uniquement s'ils se touchent !)
    # ex : [1,0,0,0] signifie que pt2 est au nord de pt1 et qu'ils se touchent
    #[0,0,0,0] signifie qu'ils ne se touchent pas 
    @staticmethod
    def get_relative_position_and_is_touching(pt1, pt2, direction) : 
        relative_position_with_direction = Points.get_relative_position_with_direction(pt1, pt2, direction)[::2] #on ne récupère que N,E,S,O
        #first check if pts are touching
        def are_touching(pt1, pt2) : 
            diff = (np.abs(pt1[0] - pt2[0]), np.abs(pt1[1] - pt2[1]))
            if 0 in diff and 1 in diff : return True 
            return False 
        return relative_position_with_direction if are_touching(pt1, pt2) else [0 for k in range(4)]
      

    #l : list of points 
    #start : head of the snake (beginning of the cycle)
    #return all possible cycle (list of list of tuples)
    @staticmethod
    def get_cycles(l, start):
        G = nx.DiGraph()
        G.add_edges_from((v1, v2) for v1 in l for v2 in l if v1 != v2 and max(abs(v1[0] - v2[0]), abs(v1[1] - v2[1])) <= 1)
        cycles = [c for c in nx.simple_cycles(G) if len(c) > 4 and start in c]
        return cycles
    
    #check if ptn inside cycle 
    #cycle : list of tuples
    @staticmethod
    def is_inside(cycle, ptn) : 
        point = Point(ptn[0], ptn[1])
        polygon = Polygon(cycle)
        return polygon.contains(point)
      
    @staticmethod 
    #cycle: list of tuples
    #ptns : list of tuples 
    #check how many ptns are in cycle 
    def n_squares(cycle, ptns) : 
      n_squares = 0 
      for ptn in ptns: 
        if Points.is_inside(cycle, ptn) : 
          n_squares += 1 
      return n_squares
    
    #cycles : list of possibles cycles, list of list of tuples (from get_cycles())
    #ptns : list of points 
    #min size : min number of squares inside cycle 
    #max size : max number of square inside cycle 
    #returns : cycles who verify n_quares between (min_size, max_size)
    @staticmethod
    def get_cycles_filtered(cycles, ptns, min_size, max_size) : 
      cycles_filtered = []
      for cycle in cycles :
        n_squares = Points.n_squares(cycle, ptns)
        if n_squares >= min_size and n_squares <= max_size : 
          cycles_filtered.append(cycle)
      return cycles_filtered
    
    
    @staticmethod
    def rotate_clockwise_n(x,y,n) : #n : number of rotations of 90 degress
      for k in range(n) : 
          x,y = y,-x
      return x,y
    
    

    
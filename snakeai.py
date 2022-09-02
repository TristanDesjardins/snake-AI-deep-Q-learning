# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 11:33:45 2022

@author: X2029440
"""

import pygame
import sys
from enum import Enum
from random import randrange
import itertools



class Color(Enum) :

  WHITE = (255, 255, 255)  # r,g,b
  BLACK = (0, 0, 0)  
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  BLUE = (0, 0, 255)


#SNAKE GAME CLASS BUT FOR THE AGENT, NOT TO PLAY MANUALLY (otherwise use snake.py)
#there are still key events to make some manual tests (but not suppose to play)
class SnakeGameAI :

  WINDOW_SIZE = 600
  MAP_SIZE = 20 #nombre de carreaux (hauteur = largeur)
  BLOCK_SIZE= WINDOW_SIZE // MAP_SIZE
  FPS = 15 #speed of the snake (number of moves/frames per sec)
  DIRECTIONS = ['UP', 'LEFT', 'DOWN', 'RIGHT'] #clockwise
  WALLS = []
  REWARDS = [10, -10, -25, 0] #reward eats fruit, reward hit wall, reward hit snake, reward nothing
  
  def __init__(self):
    
    #init window
    pygame.init()
    self.display = pygame.display.set_mode((SnakeGameAI.WINDOW_SIZE, SnakeGameAI.WINDOW_SIZE), 0, 32)
    
    #snake
    self.snake = [(SnakeGameAI.MAP_SIZE // 2, SnakeGameAI.MAP_SIZE // 2)]
    self.head = self.snake[0]
    self.direction = 'RIGHT'
    self.size_increase = 1 #how many new squares the snake has each time it eats a fruit 
    self.counter = 0 #for size increase 
    
    #scores
    self.score = 0 
    self.best_score = 0 
    
    #position of the current fruit on the map 
    self.fruit = (randrange(SnakeGameAI.MAP_SIZE), randrange(SnakeGameAI.MAP_SIZE))
    
    SnakeGameAI.WALLS = [(x,-1) for x in range(SnakeGameAI.MAP_SIZE)] + \
            [(x,SnakeGameAI.MAP_SIZE) for x in range(SnakeGameAI.MAP_SIZE)] + \
            [(-1,y) for y in range(SnakeGameAI.MAP_SIZE)] + \
            [(SnakeGameAI.MAP_SIZE,y) for y in range(SnakeGameAI.MAP_SIZE)] #coord des points du mur 

    SnakeGameAI.MAP = [(x,y) for x,y in itertools.product(range(SnakeGameAI.MAP_SIZE),range(SnakeGameAI.MAP_SIZE))]
 
  
  #draw map
  def draw_grid(self):
    self.display.fill(Color.WHITE.value)
    for x in range(0, SnakeGameAI.WINDOW_SIZE, SnakeGameAI.BLOCK_SIZE):
      for y in range(0, SnakeGameAI.WINDOW_SIZE, SnakeGameAI.BLOCK_SIZE):
        rect = pygame.Rect(x, y, SnakeGameAI.BLOCK_SIZE, SnakeGameAI.BLOCK_SIZE)
        pygame.draw.rect(self.display, Color.BLACK.value, rect, 1)




  #draw fruit in position (i,j)
  def draw_fruit(self, i, j):
    rect = pygame.Rect(i*SnakeGameAI.BLOCK_SIZE, j*SnakeGameAI.BLOCK_SIZE, SnakeGameAI.BLOCK_SIZE, SnakeGameAI.BLOCK_SIZE)
    pygame.draw.rect(self.display, Color.RED.value, rect, SnakeGameAI.BLOCK_SIZE)




  #draw snake
  def draw_snake(self):
    for square in self.snake : #draw each square of the snake
      rect = pygame.Rect(square[0] * SnakeGameAI.BLOCK_SIZE, square[1] * SnakeGameAI.BLOCK_SIZE,
                         SnakeGameAI.BLOCK_SIZE, SnakeGameAI.BLOCK_SIZE)
      pygame.draw.rect(self.display, Color.BLUE.value, rect, SnakeGameAI.BLOCK_SIZE)
      
      
      
      
  #update snake position 
  def update_snake_position(self) : 
    
    self.head = self.snake[-1][0], self.snake[-1][1]
    
    if self.direction == 'UP' :
      self.snake.append((self.head[0], self.head[1]-1))
    elif self.direction == 'DOWN' :
      self.snake.append((self.head[0], self.head[1]+1))
    elif self.direction == 'RIGHT' :
      self.snake.append((self.head[0]+1, self.head[1]))
    elif self.direction == 'LEFT' :
      self.snake.append((self.head[0]-1, self.head[1])) #right direction
      
    self.head = self.snake[-1][0], self.snake[-1][1]
    
    
    
    
  #update snake size
  #renvoie 10 si le snake a mangé, 0 sinon 
  def update_snake_size(self): 
    
    reward = SnakeGameAI.REWARDS[3]
    
    if self.head == self.fruit:
      self.score += 1
      reward = SnakeGameAI.REWARDS[0] 
      
      while self.fruit in self.snake :
        self.fruit = (randrange(SnakeGameAI.MAP_SIZE), randrange(SnakeGameAI.MAP_SIZE))
      self.counter += 1

    elif self.counter > 0 and self.counter <= self.size_increase :
      self.counter += 1
      if self.counter == self.size_increase :
        self.counter = 0

    else :
      self.snake.pop(0)

    self.draw_snake()
    
    return reward 




  #main function
  #renvoie aussi la valeur du reward à ce step et est-ce que la partie est terminée 
  #reward :
    # . 0 : nothing
    # . 10 : eats fruit
    # . -5 : hit wall 
    # . -20 : hit snake 
  #game_over = True ou False
  def update_game(self):
    
    game_over = False 
    
    self.draw_grid()
    self.draw_fruit(*self.fruit)
    self.draw_snake()
  
    self.update_snake_position()
    reward = self.update_snake_size() 
   
    is_colliding, reward_from_colliding = self.is_colliding()
    
    if is_colliding : 
      self.reset_game()
      reward = reward_from_colliding
      game_over = True 
        
    self.draw_scores()
    
    pygame.display.update() #update ui on window
    
    self.quit_window() #in case someone want to close the window
    
    return reward, game_over 
        
  
  
  
  #is_colling : whether the snake is colliding with walls or itself
  #reward : the associated reward 
  #return tuple (is_colliding, reward)
  # . -5 : hit wall 
  # . -20 : hit snake 
  def is_colliding(self): 
    has_hit_wall = self.head[0] >= SnakeGameAI.MAP_SIZE or self.head[1] >= SnakeGameAI.MAP_SIZE or \
               self.head[0] < 0 or self.head[1] < 0 #whether snake hit a wall 
    has_hit_snake = any(self.snake.count(square) > 1 for square in self.snake) #whether snake hit itself
    is_colliding = has_hit_wall or has_hit_snake
    reward_from_colliding = SnakeGameAI.REWARDS[1] if has_hit_wall \
                            else SnakeGameAI.REWARDS[2] if has_hit_snake else None 
    return is_colliding, reward_from_colliding
           
           
           
           
           
  #display score and best_score 
  def draw_scores(self) : 
    
    pygame.font.init() 
    my_font = pygame.font.SysFont('Comic Sans MS', 15)
    
    text_score = my_font.render('Score : ' + str(self.score), False, Color.RED.value)
    text_best_score = my_font.render('Best : ' + str(self.best_score), False, Color.RED.value)
    
    self.display.blit(text_score, (5,0))
    self.display.blit(text_best_score, (5,25))




  #reset game once it is over 
  def reset_game(self) : 
    
    #update best score 
    if self.score > self.best_score : 
      self.best_score = self.score
      
    self.score = 0 
    
    self.draw_grid()
    
    self.fruit = (randrange(SnakeGameAI.MAP_SIZE), randrange(SnakeGameAI.MAP_SIZE))
    self.draw_fruit(*self.fruit)
    
    self.direction = 'RIGHT'
    self.snake = [(SnakeGameAI.MAP_SIZE // 2, SnakeGameAI.MAP_SIZE // 2)]
    
    self.draw_snake()
      
  
  def update_direction_keys(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and self.direction != 'UP':
      self.direction = 'DOWN'
    elif keys[pygame.K_UP] and self.direction != 'DOWN':
      self.direction = 'UP'
    elif keys[pygame.K_LEFT] and self.direction != 'RIGHT':
      self.direction = 'LEFT'
    elif keys[pygame.K_RIGHT] and self.direction != 'LEFT':
      self.direction = 'RIGHT'
      
   
      
  def quit_window(self) : 
    #quit window
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      
      
  #game loop 
  def run_game_loop(self):

    run = True
    next_render_time = 0  #in seconds
    
    while True: #game loop 
         
      #key control 
      self.update_direction_keys() 
      
      current_time = pygame.time.get_ticks()/1000 #in seconds
      #timer to update ui 
      if  current_time >= next_render_time :  #update game only every 'FPS' seconds      
        self.update_game()     
        next_render_time = current_time + 1 / SnakeGameAI.FPS
      

if __name__ == "__main__": 
  SnakeGameAI = SnakeGameAI()
  SnakeGameAI.run_game_loop()
  
  
  
  
  
  
  
  
  
  
  
  
  
  
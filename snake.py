# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 11:33:45 2022

@author: X2029440
"""

#class to play Snake game manually


import pygame
import sys
from enum import Enum
from random import randrange

class Color(Enum) :

  WHITE = (255, 255, 255)  # r,g,b
  BLACK = (0, 0, 0)
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  BLUE = (0, 0, 255)


class SnakeGame :

  WINDOW_SIZE = 600
  MAP_SIZE = 20 #nombre de carreaux (hauteur = largeur)
  BLOCK_SIZE= WINDOW_SIZE // MAP_SIZE
  FPS = 15 #speed of the snake (number of moves/frames per sec)

  def __init__(self):
    
    #init window
    pygame.init()
    self.display = pygame.display.set_mode((SnakeGame.WINDOW_SIZE, SnakeGame.WINDOW_SIZE), 0, 32)
    
    #snake
    self.snake = [(SnakeGame.MAP_SIZE // 2, SnakeGame.MAP_SIZE // 2)]
    self.direction = None
    self.size_increase = 5 #how many new squares the snake has each time it eats a fruit 
    self.counter = 0 #for size increase 
    
    #scores
    self.score = 0 
    self.best_score = 0 
    
    #position of the current fruit on the map 
    self.fruit = (randrange(SnakeGame.MAP_SIZE), randrange(SnakeGame.MAP_SIZE))
    
    



  #draw map
  def draw_grid(self):
    self.display.fill(Color.WHITE.value)
    for x in range(0, SnakeGame.WINDOW_SIZE, SnakeGame.BLOCK_SIZE):
      for y in range(0, SnakeGame.WINDOW_SIZE, SnakeGame.BLOCK_SIZE):
        rect = pygame.Rect(x, y, SnakeGame.BLOCK_SIZE, SnakeGame.BLOCK_SIZE)
        pygame.draw.rect(self.display, Color.BLACK.value, rect, 1)




  #draw fruit in position (i,j)
  def draw_fruit(self, i, j):
    rect = pygame.Rect(i*SnakeGame.BLOCK_SIZE, j*SnakeGame.BLOCK_SIZE, SnakeGame.BLOCK_SIZE, SnakeGame.BLOCK_SIZE)
    pygame.draw.rect(self.display, Color.RED.value, rect, SnakeGame.BLOCK_SIZE)




  #draw snake
  def draw_snake(self):
    for square in self.snake : #draw each square of the snake
      rect = pygame.Rect(square[0] * SnakeGame.BLOCK_SIZE, square[1] * SnakeGame.BLOCK_SIZE,
                         SnakeGame.BLOCK_SIZE, SnakeGame.BLOCK_SIZE)
      pygame.draw.rect(self.display, Color.BLUE.value, rect, SnakeGame.BLOCK_SIZE)
      
      
      
      
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
  def update_snake_size(self): 
    
    if self.head == self.fruit:
      self.score += 100
      
      if len(self.snake) == SnakeGame.MAP_SIZE**2 : 
        print('game finished!')
        self.reset_game()
      
      while self.fruit in self.snake :
        self.fruit = (randrange(SnakeGame.MAP_SIZE), randrange(SnakeGame.MAP_SIZE))
      self.counter += 1

    elif self.counter > 0 and self.counter <= self.size_increase :
      self.counter += 1
      if self.counter == self.size_increase :
        self.counter = 0

    else :
      self.snake.pop(0)

    self.draw_snake()




  #main function
  def update_game(self):
    
    self.draw_grid()
    self.draw_fruit(*self.fruit)
    self.draw_snake()
  
    if self.direction != None : 
      self.update_snake_position()
      self.update_snake_size() 
     
      if self.is_colliding():
        self.reset_game()
        
    self.draw_scores()
        
  
  
  
  #whether the snake is colliding with walls or itself
  def is_colliding(self): 
    return self.head[0] >= SnakeGame.MAP_SIZE or self.head[1] >= SnakeGame.MAP_SIZE or \
           self.head[0] < 0 or self.head[1] < 0 or \
           any(self.snake.count(square) > 1 for square in self.snake) 
           
           
           
           
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
    
    self.fruit = (randrange(SnakeGame.MAP_SIZE), randrange(SnakeGame.MAP_SIZE))
    self.draw_fruit(*self.fruit)
    
    self.direction = None
    self.snake = [(SnakeGame.MAP_SIZE // 2, SnakeGame.MAP_SIZE // 2)]
    
    self.draw_snake()
    
    
    
  #update direction of the snake based on arrow keys events
  def update_direction(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and self.direction != 'UP':
      self.direction = 'DOWN'
    elif keys[pygame.K_UP] and self.direction != 'DOWN':
      self.direction = 'UP'
    elif keys[pygame.K_LEFT] and self.direction != 'RIGHT':
      self.direction = 'LEFT'
    elif keys[pygame.K_RIGHT] and self.direction != 'LEFT':
      self.direction = 'RIGHT'


  #game loop 
  def run_game(self):

    run = True
    next_render_time = 0  #in seconds
    while run: #game loop 
    
      current_time = pygame.time.get_ticks()/1000 #in seconds
      
      #key press events(/!\ outside the timer, we want key events to be listened at any time, not
      #only every 'FPS' seconds)
      self.update_direction() 

      #timer to update ui 
      if  current_time >= next_render_time :  #update game only every 'FPS' seconds
        self.update_game()
        pygame.display.update()
        next_render_time = current_time + 1 / SnakeGame.FPS
        
      #quit window
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
          pygame.quit()
          sys.exit()



SnakeGame = SnakeGame()
SnakeGame.run_game()
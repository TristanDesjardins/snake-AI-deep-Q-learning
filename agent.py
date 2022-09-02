# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 22:19:01 2022

@author: X2029440
"""
from snakeai import SnakeGameAI
from qnetwork import QNet, QTrainer
from points import Points
import time 
import random 
import numpy as np 
import torch 
from collections import deque
import pygame 
import datetime


#Notre agent est en quelque sorte notre IA 
#elle doit être forte pour n'importe quel 'game'
#on peut la réutiliser dans des 'games' différents
#elle n'est donc pas caractérisé par un game (pas de 'self.game')
class Agent : 
  
  BATCH_SIZE = 100_000
  MAX_MEMOMERY = 200
  
  
  
  def __init__(self) : 
    
    self.snakegameai = SnakeGameAI()
    self.qnetwork = QNet(input_size=16, output_size=3) #notre q model 
    self.qtrainer = QTrainer(self.qnetwork, 1e-3, 0.9) #model, lr, gamma
    self.epsilon = 0 #tradeoff between exploration / exploitation 
    self.nb_games = 0 #nombre de parties jouées
    self.memory = deque(maxlen=Agent.MAX_MEMOMERY)
    self.slow_down = False #whether or not to slow down learning process (to better see the UI)
    
  
  #change snake direction base on the action from our q network 
  def perform_action(self, game,action) : #action : 0, 1 ou 2  
    if action == 0 : 
      index = SnakeGameAI.DIRECTIONS.index(game.direction)
      game.direction = SnakeGameAI.DIRECTIONS[(index + 1)%4]
    elif action == 1 : return #on ne fait rien 
    elif action == 2 : 
      index = SnakeGameAI.DIRECTIONS.index(game.direction)
      game.direction = SnakeGameAI.DIRECTIONS[(index - 1)%4]
      
      
  #what is the action to take given a specific game_state for a game ? 
  #returns vector of size 3 
  def get_action(self, game_state) : 
    # random moves: tradeoff exploration / exploitation
    self.epsilon = 80 - self.nb_games
    action = [0,0,0]

    if random.randint(0, 200) < self.epsilon: #exploration (mouvement aléatoire)
      # print('exploration')
      move = random.randint(0, 2)
      action[move] = 1

    else: #exploitation (on utilise le modèle)
      # print('exploitation')
      game_state_tensor = torch.tensor(game_state, dtype=torch.float)
      prediction = self.qnetwork(game_state_tensor)
      move = torch.argmax(prediction).item()
      action[move] = 1

    return action
  
  
      
  '''
  check wether there is a close zone next to the snake (we want to avoid them, because we don't want 
  the snake to be stuck in one of them)
  min_size : min number of squares inside the close zone to be considered as such 
  max_size : max number of squares inside the close zone to be considered as such
  closed zone : [in front, left, right]
  returns : ex : [0,1,0] -> closed zone to the left of the snake 
  '''
  def get_closed_zone_state(self, game, min_size=1, max_size=25) : 
    
    l = SnakeGameAI.WALLS + game.snake
    cycles = Points.get_cycles(l, game.head) #all possible cycles 
    
    #cycles that verify n_squares between (min_size, max_size)
    #list of list of tuples 
    cycles_filtered = Points.get_cycles_filtered(cycles, SnakeGameAI.MAP, min_size, max_size)
    
    if len(cycles_filtered) == 0 : return [0,0,0]
    
    smallest_cycle = min(cycles_filtered, key=len)
    
    if game.snake.direction == 'UP' : smallest_cycle = [Points.rotate_clockwise_n(ptn[0], ptn[1], 0) for ptn in smallest_cycle]
    elif game.snake.direction == 'LEFT' : smallest_cycle = [Points.rotate_clockwise_n(ptn[0], ptn[1], 3) for ptn in smallest_cycle]
    elif game.snake.direction == 'DOWN' : smallest_cycle = [Points.rotate_clockwise_n(ptn[0], ptn[1], 2) for ptn in smallest_cycle]
    elif game.snake.direction == 'RIGHT' : smallest_cycle = [Points.rotate_clockwise_n(ptn[0], ptn[1], 1) for ptn in smallest_cycle]
    
    max_left = 0 
    max_right = 0 
    for ptn in smallest_cycle : 
      dx_left = game.head[0] - ptn[0] 
      dx_right = - dx_left 
      if dx_left > max_left : max_left = dx_left 
      if dx_right> max_right : max_right= dx_right 
      
    if dx_right > 0 and dx_left > 0 : return [0,1,0]
    elif dx_right > 0 : return [0,0,1]
    elif dx_left > 0 : return [1,0,0]
    
    
    
    
    
      
  '''
  vecteur de taille 4
  [N, E, S, O]
  ex : [1,0,0,1] il y a un bout du serpent (carré) au nord et et à l'ouest de sa tête (nord par rapport à lui)
  '''
  def get_tail_state(self,game) : 
    tail_state = [0 for k in range(4)]
    for square in game.snake[:-3] : 
      points = Points.get_relative_position_and_is_touching(game.head, square, game.direction)
      tail_state = [x + y for x, y in zip(tail_state, points)]
    return tail_state
  

  '''
  idem tail_state mais pour les murs
  '''
  def get_wall_state(self,game) : 
    wall_state = [0 for k in range(4)]
    for square in SnakeGameAI.WALLS : 
      points = Points.get_relative_position_and_is_touching(game.head, square, game.direction)
      wall_state = [x + y for x, y in zip(wall_state, points)]  
    return wall_state
  
  
  '''
  [N, NE, E, SE, S, SO, O, NO]
  vector of size 8 : ex : [0,1,0,0,0,0,0,0] le fruit est au NE du snake (NE par rapport au serpent)
  '''
  def get_fruit_state(self,game) : 
    return Points.get_relative_position_with_direction(game.head, game.fruit, game.direction)
     
  
  '''
  1 - Horizontal orientation from the food — Is the snake currently to the left or right of the food?
  2 - Vertical orientation — Is the snake currently above or below the food?
  3 - Are there walls or tails in the adjacent (left, right, above, below) squares?
  '''
  def get_game_state(self,game) : 
    
    fruit_state = self.get_fruit_state(game) #size 8
    tail_state = self.get_tail_state(game) #size 4
    wall_state = self.get_wall_state(game) #size 4
    # closed_zone_state = self.get_closed_zone_state(game) #size 3

    game_state = fruit_state + tail_state + wall_state #+ closed_zone_state

    return game_state #vecteur de taille 19
  
  
  #remember previous tuples to retrain whole network with them every time the game is over 
  def remember(self, current_state, action, reward, next_state, game_over):
    self.memory.append((current_state, action, reward, next_state, game_over)) # popleft if MAX_MEMORY is reached
  
  
  #after each gameover, train network on a whole batch 
  def train_batch(self) : 
    
      if len(self.memory) > Agent.BATCH_SIZE: batch = random.sample(self.memory, Agent.BATCH_SIZE) # list of tuples
      else: batch = self.memory
      
      states, actions, rewards, next_states, game_overs = zip(*batch)
      print(len(states))
      self.qtrainer.train(states, actions, rewards, next_states, game_overs)
      
      
  def get_mouse_wheel_events(self) : 
    for event in pygame.event.get():
      if event.type == pygame.MOUSEWHEEL:
        if event.y == 1 : self.slow_down = False 
        if event.y == -1 : self.slow_down = True
    if self.slow_down : 
      time.sleep(0.05)

      
  #save our qnetwork 
  def save_model(self, model_path) : 
    torch.save(self.qnetwork.state_dict(), model_path)
    print('model saved')
      
    
  #make agent train from existing qnetwork model rather than starting from 0
  def train_agent_from_model(self, model_path, game) : 
    self.qnetwork = QNet()
    self.qnetwork.load_state_dict(torch.load(model_path))
    self.qtrainer = QTrainer(self.qnetwork, 1e-3, 0.9) #model, lr, gamma
    self.train_agent(game)
  
  
  
  #train the agent on a game 
  def train_agent(self,game) :

    try : 
      #training 
      while True :
        
        seconds = int(pygame.time.get_ticks()/1000)
        print("AI've been training for:", datetime.timedelta(seconds=seconds))
        print("AI've played", self.nb_games,'games')
        
        current_state = self.get_game_state(game)  
        print(current_state)
        action = self.get_action(current_state)

        # game.update_direction_keys() #changer direction avec les keys 
        self.perform_action(game, np.argmax(action)) #change direction      
        reward, game_over = game.update_game()
        
        if game_over : 
          a.nb_games += 1   
        
        next_state = self.get_game_state(game)  
        self.remember(current_state, action, reward, next_state, game_over) #remember tuple to retrain whole qnetwork later   
        self.qtrainer.train(current_state, action, reward, next_state, game_over) #train short memory 
   
        #EXPERIENCE REPLAY 
        #on réentraine sur un sample de batch_size element de notre mémoire (ce qu'on appelle aussi 'train long memory')
        #cette étape n'est pas obligatoire mais c'est quand même beaucoup plus efficace
        if game_over : 
          self.train_batch() #prend un peu de temps d'où les petites pauses entre chaque partie
          
        self.get_mouse_wheel_events() #to speed or slow the learning process 

        
    finally :  #on exiting the program 
      self.save_model('qnetwork.pt')
      
      
      
 
    
    
if __name__ == "__main__" : 
  
  a = Agent()
  
  game = SnakeGameAI()
  
  # model_path = 'qnetwork.pt'
  # a.train_agent_from_model(model_path, game)
  
  a.train_agent(game) #train from 0 
  
  
      

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
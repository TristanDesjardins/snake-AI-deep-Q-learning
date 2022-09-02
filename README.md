# Snake game AI - Deep reinforcement learning
Snake AI using deep reinforcement learning (deep Q learning) with pytorch and pygame. It was a challenge I gave myself. 

## Preview 
**training phase**             |  **After training**
:-------------------------:|:-------------------------:
![snake_training](https://user-images.githubusercontent.com/62900180/188200059-ff49ed8b-711b-42bb-ab50-9f377f042d38.gif) | ![snake_trained](https://user-images.githubusercontent.com/62900180/188200076-e9532f77-b97a-4be6-8db5-6fb16e791a16.gif)

## General Idea 
We've created a deep neural network (qnetwork.py) which is attached to our snake. At each step in the game, we feed the neural network a **game state** which gives our snake (agent) information about its environment. The game state is a vector of size 16 giving information about relative position of the fruit, the walls and the snake itself to the head of the snake. Each action leads to a different reward (hitting wall, eating fruit, hitting itself, nothing). We then optimize our qnetwork using gradient descent based on Bellman's equation. 

## Main files
- agent.py : to train the AI (or agent) 
- snakegame.py : in case you just want to play the game yourself, run that file 
- snakegameai.py : like snakegame.py but with AI instead of key events 


## Installation  
- Python 3.9.12
- [pygame 2.1.2](https://www.pygame.org/news) : for the game engine 
- [pytorch 0.4.1](https://pytorch.org/) : for the AI (Q Network) 

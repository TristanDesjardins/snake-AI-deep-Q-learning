# snake-AI-deep-Q-learning
Snake AI using deep reinforcement learning (deep Q learning) with pytorch and pygame. It was a challenge I gave myself. Enjoy! :blush:

## Preview 

Just run the 'agent.py' file to see our snake (agent) training within a few minutes! :blush: <br/>
That should look a lil' something like this: 

<img src="https://user-images.githubusercontent.com/62900180/187643756-457e874a-85a9-4fd9-bba5-f750499b2135.gif" height="400">

## Main files
- agent.py : to train the AI (or agent) 
- snakegame.py : in case you just want to play the game yourself, run that file 
- snakegameai.py : like snakegame.py but with AI instead of key events 

## General Idea 
We've created a deep neural network (qnetwork.py) which is attached to our snake. At each step in the game, we feed the neural network a **game state** which gives our snake (agent) information about its environment. The game state is a vector of size 16 giving information about relative position of the fruit, the walls and the snake itself to the head of the snake. Each action leads to a different reward (hitting wall, eating fruit, hitting itself, nothing). We then optimize our qnetwork using gradient descent based on Bellman's equation. 

## Installation  

- Python 3.8.10

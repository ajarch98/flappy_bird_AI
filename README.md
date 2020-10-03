# flappy_bird_AI

The goal of this project is to test the NEAT (Neuro-Evolution of Augmenting Topologies) algorithm on a Flappy Bird clone. This is achieved entirely in Python, using the pygame and neat-python libraries.

I completed this project in two phases:
1. Building the Flappy Bird clone using pygame
2. Integrating neat-Python into the final code

## About NEAT

NEAT is an acronym for Neuro-Evolution of Augmenting Technologies. It is an evolution algorithm. 

It operates by:
- creating a generation containing multiple instances of objects
- tracking the 'fittest' instance
- 'breeding' the fittest instances to create the subsequent generation

## How to run
- Install Python 3
- Clone repository
- Install requirements
- [Optional] Run the game using the function FlappyBird.play()
- Train AI using the function FlappyBird.train_ai()

## Interesting observations
- The most tortuous section of building the program involved creating a `Game Over` screen
- I made the game as hard as possible, to the point where I cannot pass a single pipe. However, the AI learns the game in less than 10 generations. 

## Attributions:
- Inspired by and remixed from https://github.com/techwithtim/NEAT-Flappy-Bird/blob/master/flappy_bird.py

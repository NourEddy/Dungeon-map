# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 15:57:08 2023

@author: Nour Eddine
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:48:09 2023

@author: Nour Eddine
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:24:20 2023

@author: Nour Eddine
"""

import numpy as np
import argparse

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = {}

    def get_action(self, state):
        """
        Get the action with the highest Q-value for the given state.
        """
        state = str(state)
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.actions)
        else:
            return self.get_max_Q(state)[1]


    def get_max_Q(self, state):
        """
        Get the maximum Q-value for the given state.
        """
        state = str(state)
        max_Q = -float('inf')
        max_action = None
        for action in self.actions:
            Q = self.Q.get((state, action), 0)
            if Q > max_Q:
                max_Q = Q
                max_action = action
        return max_Q, max_action



    def learn(self, state, action, reward, next_state):
        """
        Update the Q-value for the state-action pair using the Q-learning update rule.
        """
        state = str(state)
        next_state = str(next_state)
        max_Q, _ = self.get_max_Q(next_state)
        Q = self.Q.get((state, action), 0)
        self.Q[(state, action)] = Q + self.alpha * (reward + self.gamma * max_Q - Q)
    

class DungeonMapGenerator:
    def __init__(self, agent, map_size=4, treasure_location=(3,3)):
        self.agent = agent
        self.map_size = map_size
        self.current_state = None
        self.treasure_location = treasure_location
        self.treasure_found = False
        self.game_over = False
        self.steps = 0
        self.max_steps = map_size * map_size
        self.rewards = {
            'treasure': 1,
            'wall': -1,
            'step': -0.1
        }

    def reset(self):
        """
        Reset the map to its initial state
        """
        self.current_state = np.zeros((self.map_size, self.map_size))
        self.treasure_found = False
        self.game_over = False
        self.steps = 0

    def get_next_state(self, action):
        """
        Update the map based on the action taken
        """
        x, y = self.current_state.nonzero()
        if action == "up":
            x -= 1
        elif action == "down":
            x += 1
        elif action == "left":
            y -= 1
        elif action == "right":
            y += 1
        if x<0 or x>=self.map_size or y<0 or y>=self.map_size:
            reward = self.rewards['wall']
            next_state = self.current_state
        else:
            next_state = np.zeros((self.map_size, self.map_size))
            next_state[x, y] = 1
            if (x,y) == self.treasure_location:
                reward = self.rewards['treasure']
                self.treasure_found = True
            else:
                reward = self.rewards['step']
        return next_state, reward

    def is_game_over(self):
        """
        Check if the game is over (either the treasure has been found or the agent has run out of moves)
        """
        self.game_over =  self.treasure_found or (self.steps>=self.max_steps)
        return self.game_over

    def play(self):
        """
        Play the game and train the agent
        """
        self.reset()
        while not self.is_game_over():
            action = self.agent.get_action(self.current_state)
            next_state, reward = self.get_next_state(action)
            self.agent.learn(self.current_state, action, reward, next_state)
            self.current_state = next_state
            self.steps += 1
            
    
    
def main(args):
    # Define the possible actions the agent can take
    actions = ["up", "down", "left", "right"]

    # Initialize the Q-learning agent
    agent = QLearningAgent(actions, epsilon=args.epsilon)
    #agent = QLearningAgent(actions, epsilon=0.1)

    # Initialize the dungeon map generator
    generator = DungeonMapGenerator(agent, map_size=args.map_size, treasure_location=args.treasure_location)


    # Play the game and train the agent
    for i in range(args.num_games):
        generator.play()
        if i % 100 == 0:
            print(f'Game {i+1} completed')
    print("Training completed!")

    # Print the learned Q-values
    #print(agent.Q)

    # Test the agent's performance
    generator.reset()
    while not generator.is_game_over():
        action = agent.get_action(generator.current_state)
        next_state, _ = generator.get_next_state(action)
        generator.current_state = next_state
        generator.steps += 1
    print(f'Treasure found in {generator.steps} steps')
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dungeon Map Generator')
    parser.add_argument('--epsilon', type=float, default=0.1,
                        help='Epsilon for the Q-learning agent')
    parser.add_argument('--map_size', type=int, default=4,
                        help='Size of the map')
    parser.add_argument('--treasure_location', type=tuple, default=(3,3),
                        help='Location of the treasure on the map')
    parser.add_argument('--num_games', type=int, default=1,
                        help='Number of games to play')
    args = parser.parse_args()
    main(args)

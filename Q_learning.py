import numpy as np

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.Q = {}

    def get_max_Q(self, state):
        max_Q = -float('inf')
        max_action = None
        for action in self.actions:
            if self.Q.get((state, action)) > max_Q:
                max_Q = self.Q.get((state, action))
                max_action = action
        return max_Q, max_action

    def learn(self, state, action, reward, next_state):
        max_Q, _ = self.get_max_Q(next_state)
        self.Q[(state, action)] = (1 - self.alpha) * self.Q.get((state, action), 0) + self.alpha * (reward + self.gamma * max_Q)

class DungeonMapGenerator:
    def __init__(self, agent, map_size=4):
        self.agent = agent
        self.map_size = map_size
        self.current_state = None
        self.treasure_found = False

    def reset(self):
        # Reset the map to its initial state
        self.current_state = np.zeros((self.map_size, self.map_size))
        self.treasure_found = False

    def get_next_state(self, action):
        # Update the map based on the action taken
        x, y = self.current_state.nonzero()
        if action == "up":
            x -= 1
        elif action == "down":
            x += 1
        elif action == "left":
            y -= 1
        elif action == "right":
            y += 1
        next_state = self.current_state.copy()
        next_state[x, y] = 1
        return next_state

    def is_treasure_found(self):
        # Check if the treasure has been found
        x, y = self.current_state.nonzero()
        return (x == self.map_size - 1) and (y == self.map_size - 1)

    def is_game_over(self):
        # Check if the game is over (either the treasure has been found or the agent has run out of moves)
        return self.treasure_found or (self.current_state == 1).all()

    def play(self):
        self.reset()
        while not self.is_game_over():
            action = self.agent.get_max_Q(self.current_state)[1]
            next_state = self.get_next_state(action)
            reward = 0
            if self.is_treasure_found():
                self.treasure_found = True
                reward = 1
            self.agent.learn(self.current_state, action, reward, next_state)
            self.current_state = next_state

def main():
    # Define the possible actions the agent can take
    actions = ["up", "down", "left", "right"]

    # Initialize the Q-learning agent
    agent = QLearningAgent(actions)

    # Initialize the dungeon map generator
    generator = DungeonMapGenerator(agent)

    # Play the game and train the agent
    generator.play()

    # Print the learned Q-values
    print(agent.Q)


if __name__ == "__main__":
    main()


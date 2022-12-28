import numpy as np

# Define the state space and action space
# Each state is a tuple representing the current placement of the walls, starting point, treasure point, and ending point
# The action space is a list of tuples representing the possible movements the agent can take
states = [(w1, s, t, e) for w1 in range(5) for s in range(16) for t in range(16) for e in range(16)]
actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Initialize the Q-table with random values and set the discount factor (gamma) and the learning rate (alpha)
Q = np.random.randn(len(states), len(actions))
gamma = 0.9
alpha = 0.1

# Define the exploration rate (epsilon) and the convergence threshold
epsilon = 0.1
threshold = 0.95

# Define a function that takes in the current state and returns the best action to take based on the Q-table
def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        # Explore: choose a random action
        action = np.random.randint(0, len(actions))
    else:
        # Exploit: choose the action with the highest Q-value
        action = np.argmax(Q[state, :])
    return action

# Define a function that updates the Q-table based on the current state, the chosen action, and the resulting next state
def update_Q(state, action, reward, next_state):
    Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state, :]))

# Define a function that takes a state and an action as input and returns the reward and next state resulting from taking that action
def take_action(state, action):
    # Get the current placement of the walls, starting point, treasure point, and ending point
    w1, s, t, e = state
    
    # Get the displacement caused by the action
    dx, dy = action
    
    # Calculate the new placement of the starting point
    s_new = (s[0] + dx, s[1] + dy)
    
    # Check if the new starting point is out of bounds or if there is a wall at that location
    if s_new[0] < 0 or s_new[0] >= 4 or s_new[1] < 0 or s_new[1] >= 4 or (s_new[0], s_new[1]) in w1:
        # If the move is invalid, return a reward of -1 and the current state as the next state
        return -1, state
    else:
        # If the move is valid, update the starting point and check if the new location is the treasure point or the ending point
        if s_new == t:
            # If the new location is the treasure point, return a reward of 10 and the new state with the treasure point replaced by the starting point as the next state
            return 10, (w1, s_new, s, e)
        elif s_new == e:
            # If the new location is the ending point, return a reward of 100 and the current state as the next state
            return 100, state
        else:
            # If the new location is neither the treasure point nor the ending point, return a reward of 0 and the new state as the next state
            return 0, (w1, s_new, t, e)

# Define a function that takes a Q-table as input and generates the dungeon map by following the optimal actions from the starting point to the treasure point and then from the treasure point to the ending point
def generate_map(Q):
    # Initialize the current state with the starting point as the starting point, the treasure point as the treasure point, and the ending point as the ending point
    current_state = (w1, s, t, e)
    
    # Initialize an empty list to store the actions taken
    actions_taken = []
    
    # Follow the optimal actions from the starting point to the treasure point
    while current_state[1] != current_state[2]:
        # Choose the best action to take based on the current state
        action = np.argmax(Q[current_state, :])
        
        # Take the action and observe the reward and next state
        reward, next_state = take_action(current_state, action)
        
        # Update the current state
        current_state = next_state
        
        # Append the action to the list of actions taken
        actions_taken.append(action)
    
    # Follow the optimal actions from the treasure point to the ending point
    while current_state[1] != current_state[3]:
        # Choose the best action to take based on the current state
        action = np.argmax(Q[current_state, :])
        
        # Take the action and observe the reward and next state
        reward, next_state = take_action(current_state, action)
        
        # Update the current state
        current_state = next_state
        
        # Append the action to the list of actions taken
        actions_taken.append(action)
    
    # Return the list of actions taken
    return actions_taken

# Iterate through a loop that chooses actions based on the current state and updates the Q-table until the algorithm converges on a solution
iteration = 0
max_iterations = 1000
while True:
    # Choose an action based on the current state
    action = choose_action(current_state)

    # Take the action and observe the reward and next state
    reward, next_state = take_action(current_state, action)

    # Update the Q-table
    update_Q(current_state, action, reward, next_state)

    # Update the current state
    current_state = next_state

    # Increment the iteration counter
    iteration += 1

    # Check if the algorithm has converged and exit the loop if it has
    if np.max(Q) > threshold or iteration > max_iterations:
        break

# Use the final Q-table to generate the dungeon map
actions_taken = generate_map(Q)

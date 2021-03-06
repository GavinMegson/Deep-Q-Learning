import csv
import gym
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf
from random import randint, uniform

gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)

env = gym.make('gym_agent_vs_agent:AgentVsAgent-v0',
               primaryAgent="test", opposingAgent="random")

# Following code is adapted from Keras.io's example on applying DQN to playing
# an Atari game. Notably, the shape that the neural network is expecting had
# to be adapted which requires reshaping the output from the agent vs agent
# gym
######################
# Begin adapted code #
######################
# Configuration paramaters for the whole setup
seed = 42
gamma = 0.99  # Discount factor for past rewards
epsilon = 1.0  # Epsilon greedy parameter
epsilon_min = 0.1  # Minimum epsilon greedy parameter
epsilon_max = 1.0  # Maximum epsilon greedy parameter
epsilon_interval = (
    epsilon_max - epsilon_min
)  # Rate at which to reduce chance of random action being taken
batch_size = 32  # Size of batch taken from replay buffer
max_steps_per_episode = 10000
model_name = 'model-rnn-c-tox'

# Number of actions needed to be adapted since the Showdown Simulator has more
# moves than an Atari game
num_actions = 9


def create_q_model():
    # Network defined by the Deepmind paper
    # Old and new shapes
    #inputs = layers.Input(shape=(84, 84, 4,))
    inputs = layers.Input(shape=(54, 1,))

    # layer1 = layers.Conv1D(32, 8, strides=2, activation="relu")(inputs)
    # layer2 = layers.Conv1D(64, 4, strides=2, activation="relu")(layer1)

    # layer4 = layers.Flatten()(layer2)
    # Convolutions on the states of the Pokemon game
    layerA = layers.LSTM(1024, return_sequences=True)(inputs)
    layerB = layers.Flatten()(layerA)

    layer4 = layers.Dense(512, activation="relu")(layerB)
    layer5 = layers.Dense(128, activation="relu")(layer4)
    layer6 = layers.Dense(64, activation="relu")(layer5)
    layer7 = layers.Dense(32, activation="relu")(layer6)
    action = layers.Dense(num_actions, activation="linear")(layer7)

    return keras.Model(inputs=inputs, outputs=action)


def load_q_model(filename):
    return keras.models.load_model(filename)


# The first model makes the predictions for Q-values which are used to
# make a action.

model = create_q_model()
#model = load_q_model(model_name)

# Build a target model for the prediction of future rewards.
# The weights of a target model get updated every 10000 steps thus when the
# loss between the Q-values is calculated the target Q-value is stable.

model_target = create_q_model()
#model_target = load_q_model(model_name)

# In the Deepmind paper they use RMSProp however then Adam optimizer
# improves training time
optimizer = keras.optimizers.Adam(learning_rate=0.0025, clipnorm=1.0)

# Experience replay buffers
action_history = []
state_history = []
state_next_history = []
rewards_history = []
done_history = []
episode_reward_history = []
running_reward = 0
episode_count = 0
game_count = 0
# Number of game states to take random action and observe output
epsilon_random_games = 10000
# Number of game states for exploration
epsilon_greedy_games = 1000000.0
# Maximum replay length
# Note: The Deepmind paper suggests 1000000 however this causes memory issues
max_memory_length = 100000
# Train the model after 4 actions
update_after_actions = 4
# How often to update the target network
update_target_network = 5000
# Using huber loss for stability
loss_function = keras.losses.Huber()

save_model_checkmark = 10000

while True:  # Run until solved
    state = np.array(env.reset())
    episode_reward = 0

    for timestep in range(1, max_steps_per_episode):
        # env.render(); Adding this line would show the attempts
        # of the agent in a pop up window.
        game_count += 1

        if game_count < epsilon_random_games or epsilon > np.random.rand(1)[0]:
            # Take random action
            action = np.random.choice(num_actions)
            if uniform(0, 1) < 0.9:
                action = randint(0, 3)
            else:
                action = randint(4, 8)
        else:
            # Predict action Q-values
            # From environment state
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, 0)
            action_probs = model(state_tensor, training=False)
            # Take best action
            action = tf.argmax(action_probs[0]).numpy()

        # Decay probability of taking random action
        epsilon -= epsilon_interval / epsilon_greedy_games
        epsilon = max(epsilon, epsilon_min)

        # Apply the sampled action in our environment
        state_next, reward, done, _ = env.step(action)
        template = "rr: {:.2f} r: {:.2f} ep: {}, gc {}"
        print(template.format(running_reward, reward, episode_count, game_count))
        state_next = np.array(state_next)

        episode_reward += reward

        # Save actions and states in replay buffer
        action_history.append(action)
        state_history.append(state)
        state_next_history.append(state_next)
        done_history.append(done)
        rewards_history.append(reward)
        state = state_next

        # Update every fourth game and once batch size is over 32
        if game_count % update_after_actions == 0 and len(done_history) > batch_size:

            # Get indices of samples for replay buffers
            indices = np.random.choice(
                range(len(done_history)), size=batch_size)

            # Using list comprehension to sample from replay buffer
            state_sample = np.array([state_history[i]
                                     for i in indices], dtype=object)
            if state_sample.shape == (32,):
                state_sample = np.stack(state_sample)
            state_sample = state_sample.astype('int32')
            state_sample = state_sample.reshape([1, 32, 54, 1])
            state_next_sample = np.array(
                [state_next_history[i] for i in indices], dtype=object)
            if state_next_sample.shape == (32,):
                state_next_sample = np.stack(state_next_sample)
            state_next_sample = state_next_sample.astype('int32')
            #state_next_sample = state_next_sample.reshape([1]+list(state_next_sample.shape)+[1])
            state_next_sample = state_next_sample.reshape([1, 32, 54, 1])
            rewards_sample = [rewards_history[i] for i in indices]
            action_sample = [action_history[i] for i in indices]
            done_sample = tf.convert_to_tensor(
                [float(done_history[i]) for i in indices]
            )

            # Build the updated Q-values for the sampled future states
            # Use the target model for stability
            future_rewards = model_target.predict(state_next_sample[0])
            # Q value = reward + discount factor * expected future reward
            updated_q_values = rewards_sample + gamma * tf.reduce_max(
                future_rewards, axis=1
            )

            # If final game set the last value to -1
            updated_q_values = updated_q_values * \
                (1 - done_sample) - done_sample

            # Create a mask so we only calculate loss on the updated Q-values
            masks = tf.one_hot(action_sample, num_actions)

            with tf.GradientTape() as tape:
                # Train the model on the states and updated Q-values
                q_values = model(state_sample[0])

                # Apply the masks to the Q-values to get the Q-value for action taken
                q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
                # Calculate loss between new Q-value and old Q-value
                loss = loss_function(updated_q_values, q_action)

            # Backpropagation
            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))

        if game_count % update_target_network == 0:
            # update the the target network with new weights
            model_target.set_weights(model.get_weights())
            # Log details
            template = "running reward: {:.2f} at episode {}, game count {}"
            print(template.format(running_reward, episode_count, game_count))

        if game_count % save_model_checkmark == 0:
            model.save(model_name)

        # Limit the state and reward history
        if len(rewards_history) > max_memory_length:
            print("**************************\nHERE\n**************************")
            del rewards_history[:1]
            del state_history[:1]
            del state_next_history[:1]
            del action_history[:1]
            del done_history[:1]

        if done:
            break

    # Update running reward to check condition for solving
    episode_reward_history.append(episode_reward)
    if len(episode_reward_history) > 10000:
        del episode_reward_history[:1]
    running_reward = np.mean(episode_reward_history)

    episode_count += 1

    if running_reward > 1000:  # Condition to consider the task solved
        print(f"Solved at episode {episode_count}!")
        break
####################
# end adapted code #
####################

model.save(model_name)

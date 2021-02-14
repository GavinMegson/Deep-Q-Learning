import gym
import numpy as np
from showdown_simulator import ShowdownSimulator
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

class AgentVsAgentEnv(gym.Env):
    NUM_OBSERVABLE_FEATURES = 120
    CAP = 10000
    def __init__(self, primaryAgent, opposingAgent):
        self.primaryAgent = primaryAgent
        self.opposingAgent = opposingAgent
        self.action_space = gym.spaces.Discrete(9)
        self.observation_space = gym.spaces.Box(low=0, high=self.CAP, shape=(self.NUM_OBSERVABLE_FEATURES,), dtype=np.int)

    def step(self, action):
        self._take_action(action)
       
       
        reward = self.simulator.primaryAgentReward() 

        # Check if the match is over
        done = self.simulator.matchOver()

        obs = self._next_observation("primary")

        return obs, reward, done, {}

    def _take_action(self, action):
        obs = self._next_observation("opposing")
        opponentAction, _ = self.opponentAgent.predict(obs)
        self.simulator.upate(action, opponentAction)

    def reset(self):
        self.simulator = ShowdownSimulator()
        self.simulator.setup(self.primaryAgent, self.opposingAgent)
        return self._next_observation(self.primaryAgent)

    def _next_observation(self, player):
        return self.simlator.summarize(player)

    def render(self, mode='human', close=False):
        print(self.simulator.render())


env = AgentVsAgentEnv()

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=20000)

obs = env.reset()
for i in range(2000):
    action, _states = model.predict(obs)
    print(action)
    obs, rewards, done, info = env.step(action)
    env.render

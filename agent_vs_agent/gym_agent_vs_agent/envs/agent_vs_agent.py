import gym
import numpy as np
from showdown_simulator import ShowdownSimulator
class AgentVsAgent(gym.Env):
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

        obs = self._next_observation()

        return obs, reward, done {}

    def _take_action(self, action):
        obs = self._next_observation()
        opponentAction, _ = self.opponentAgent(obs)
        self.simulator.upate(action, opponentAction)

    def reset(self):
        self.simulator = ShowdownSimulator()
        self.simulator.setup(primaryAgent, opposingAgent)
        return self._next_observation()

    def _next_observation(self):
        return self.simlator.summarize()

    def render(self, mode='human', close=False):
        print(self.simulator.render())


AgentVsAgent()

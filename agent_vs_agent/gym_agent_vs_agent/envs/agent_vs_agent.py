import gym
import numpy as np
from gym_agent_vs_agent.envs.showdown_simulator import ShowdownSimulator
from gym_agent_vs_agent.envs.random_agent import RandomAgent


class AgentVsAgentEnv(gym.Env):
    NUM_OBSERVABLE_FEATURES = 120
    CAP = 10000

    def __init__(self, primaryAgent, opposingAgent):
        self.primaryAgent = primaryAgent
        if opposingAgent == "random":
            self.opposingAgent = RandomAgent()
        self.action_space = gym.spaces.Discrete(9)
        self.observation_space = gym.spaces.Box(
            low=0, high=self.CAP, shape=(self.NUM_OBSERVABLE_FEATURES,), dtype=np.int)

    def step(self, action):
        self._take_action(action)

        reward = self.simulator.primaryAgentReward()

        # Check if the match is over
        done = self.simulator.matchOver

        obs = self._next_observation("primary")

        return obs, reward, done, {}

    def _take_action(self, action):
        obs = self._next_observation("opposing")
        opponentAction, _ = self.opposingAgent.predict(obs)
        self.simulator.update(action, opponentAction)

    def reset(self):
        self.simulator = ShowdownSimulator()
        self.simulator.setup()
        return self._next_observation(self.primaryAgent)

    def _next_observation(self, player):
        return self.simulator.summarize(player)

    def render(self, mode='human', close=False):
        print(self.simulator.render())


#env = AgentVsAgentEnv()
#
#model = PPO2(MlpPolicy, env, verbose=1)
# model.learn(total_timesteps=20000)
#
#obs = env.reset()
# for i in range(2000):
#    action, _states = model.predict(obs)
#    print(action)
#    obs, rewards, done, info = env.step(action)
#    env.render

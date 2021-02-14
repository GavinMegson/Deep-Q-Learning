from gym.envs.registration import register

register(
    id='AgentVsAgent-v0',
    entry_point='gym_agent_vs_agent.envs:AgentVsAgentEnv',
)

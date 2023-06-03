from agent import Agent
from pettingzoo.butterfly import cooperative_pong_v5
import requests
import json

env = cooperative_pong_v5.parallel_env(render_mode="human")

agent_urls = {
    "agent_0": "http://localhost:5000/select_action",
    "agent_1": "http://localhost:5001/select_action",
}


def get_action(agent, action_space):
    while True:
        try:
            resp = requests.post(agent_urls[agent], json.dumps(action_space))
            resp.raise_for_status
            return resp.json()
        except requests.exceptions.RequestException:
            print(f"Couldn't connect to agent {agent}, retrying...")
            continue


for i in range(10):
    observations = env.reset()
    print(f"game: {i}")

    while env.agents:
        actions = {}
        for agent in env.agents:
            action_space = env.action_spaces(agent)
            actions[agent] = get_action(agent, action_space)
        observations, rewards, terminations, truncations, infos = env.step(
            actions)
        env.render()
env.close()

from pettingzoo.butterfly import cooperative_pong_v5
import requests
import jsonpickle as json
import time

env = cooperative_pong_v5.parallel_env(render_mode="rgb_array")

agent_urls = {
    "paddle_0": "http://agent_1:5000/select_action",
    "paddle_1": "http://agent_2:5001/select_action",
}


def get_action(agent, action_space):
    while True:
        try:
            resp = requests.post(agent_urls[agent], json.dumps(action_space))
            print(json.loads(resp.text))
            resp.raise_for_status
            return json.loads(resp.text)
        except requests.exceptions.RequestException:
            print(f"Couldn't connect to agent {agent}, retrying...")
            time.sleep(1)
            continue


for i in range(10):
    observations = env.reset()
    print(f"game: {i}")

    while env.agents:
        actions = {}
        for agent in env.agents:
            action_space = env.action_space(agent)
            actions[agent] = get_action(
                agent, action_space)
        observations, rewards, terminations, truncations, infos = env.step(
            actions)
        env.render()
env.close()

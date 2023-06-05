"""
This is an agent class that can be used to create an agent for the pettingzoo environment.
The agent is a simple random agent that selects a random action from the action space.
The agent is created by passing an agent_id to the constructor.
The agent_id is used to identify the agent in the environment.
The agent has a select_action method that takes an action_space as input and returns an action.
The action_space is a dictionary that contains the action space for each agent in the environment.
The action is a dictionary that contains the action for each agent in the environment.
The action is a random action from the action space.
The select_action method can be called by the environment via http requests.
The expected arguments are an agent_id and the port for the agent to listen on.
"""

import jsonpickle as json
from flask import Flask, request
import sys


class Agent:
    def __init__(self, agent_id):
        print("agent " + agent_id + " is created!")
        self.agent_id = agent_id

    def select_action(self, action_space):
        return action_space.sample()


app = Flask(__name__)
agent = Agent(sys.argv[1])


@app.route('/')
def healt():
    return 'App works!'


@app.route('/select_action', methods=['POST'])
def select_action():
    action_space = json.loads(request.data)
    action = agent.select_action(action_space)
    return json.dumps(action)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=sys.argv[2])

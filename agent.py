"""
This class defines a random agent for the 'pettingzoo' environment.
An agent is instantiated with an 'agent_id' for identification.
It has a 'select_action' method which picks a random action from the provided action_space dictionary.
The action_space dictionary details the available actions for each agent.
The chosen action is a dictionary format.
This method can be invoked by the environment through HTTP requests, expecting 'agent_id' and a listening port as arguments.
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
@app.route('/' + agent.agent_id)
def status():
    return 'App works! for ' + agent.agent_id


@app.route('/health')
@app.route('/' + agent.agent_id + '/health')
def health():
    return 'Heartbeat for ' + agent.agent_id + ' is OK!'


@app.route('/select_action', methods=['POST'])
def select_action():
    action_space = json.loads(request.data)
    action = agent.select_action(action_space)
    return json.dumps(action)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(sys.argv[2]))

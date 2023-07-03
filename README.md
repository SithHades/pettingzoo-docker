# Pettingzoo Docker Images

This project provides a starting point to split your pettingzoo multia agent environment into agent and environment containers.
The assumption is, that agents, specifically in deep reinforcement learning can get quite complex, and it can be beneficial to split the agent from the environment.

## How to use

The project is split into two parts, the agent and the environment. The agent is a simple flask server, that can be used by the environment. While the agent takes a name and a port number as arguments, the environments means of connection to the agents depend on the specified url and the docker network configuration.

To start the agents, simply run the following command:

```bash
docker build -t agent -f dockerfile.agent .
docker run -d --name agent_1 -p 5000:5000 agent agent_1 5000
docker run -d --name agent_2 -p 5001:5000 agent agent_2 5001
```

Then, you can start the environment by running:

```bash
docker build -t env -f dockerfile.env .
docker run -it env
```

Depending on your docker network configuration there can be an issue, preventing the environment from connecting to the agents. To fix this, you can create a new network and add the agents to it:

```bash
docker network create myNetwork
docker network connect myNetwork agent_1
docker network connect myNetwork agent_2
```

Then, you can start the environment by running (build, if still necessary):

```bash
docker run -it --network myNetwork env
```

## Further Information

The render mode of the environment had to be set to `rgb_array`, because the docker container for the environment does not have a display by default. This means, that the environment can not be rendered in `human` mode.

# MCP server for interaction with Nao robot

This repository contains the implementation of a MCP server to communicate with a Nao robot (actually it should work on any robot running Naoqi, the OS embedded in all Aldebaran robots).

It focuses mainly on interactive high level APIs to allow the implementation of the interaction with the robot based on AI agents.

> [!IMPORTANT]
> This has only been tested with Naoqi 2.1.4.13 on a Nao v5.
> Qi package should work with no problem on more recent versions of Naoqi, however the Naoqi API used here might have evolved since version 2.1.4.13. To test it and add compatibility, a Nao v6 robot (or even a Pepper robot) would be needed ! 🙂

# Content

- MCP server for communication with a Nao robot
    - implementation in file [https://github.com/funwithagents/nao-mcp/src/nao_mcp/server.py](https://github.com/funwithagents/nao-mcp/src/nao_mcp/server.py)

# Installation

- clone the repository or download the source code
- to connect to a real Nao robot, you will need to install the `qi` python package.
    - you can find the built package corresponding to your setup (MacOS or Linux, and Python version) in the [latest Release](https://github.com/funwithagents/libqi-python/releases) of this [fork](https://github.com/funwithagents/libqi-python) of the [official libqi-python repository](https://github.com/aldebaran/libqi-python) (that was not maintained)
    - for the moment, it it only compatible with MacOS arm64 and Linux architectures
    - download the corresponding .whl file
    - install it in your python setup : `pip install path/to/download/wheel.whl`

> [!NOTE]
> If you do not have a Nao (how unlucky… 😅), or if your current setup is not (yet ?) supported by the provided builds of qi package (for example if you are on Windows, hey we won’t judge), don’t worry, you can still use this MCP server with a “fake” robot !
> See usage below.

# Usage

- run the MCP server with a real Nao robot
    - connect you Nao to your network
    - retrieve its IP address (by pressing its torso button) ⇒ `<nao-ip>`
    - run the server : `python server.py --ip <nao-ip>`

- if you don’t have a Nao robot or if your current setup is not compatible with the available qi pacakges, you can run the MCP server with a “fake” robot ⇒ all the MCP tools will be available for execution, they will just do nothing real.
    - run the server in “fake” robot mode :  `python server.py --fake-robot`

## Usage with Claude Desktop

As any MCP server, you can add it to Claude Desktop. To do so, you will need to add it to your `claude_desktop_config.json` file.

- for a real robot
    
    ```json
    "mcpServers": {
        "nao-mcp": {
            "command": "python",
          "args": [
            "path/to/repo/src/nao_mcp/server.py",
            "--ip <nao-ip>"
          ]
        }
    }
    ```
    
- for fake robot mode
    
    ```json
    "mcpServers": {
        "nao-mcp": {
            "command": "python",
          "args": [
            "path/to/repo/src/nao_mcp/server.py",
            "--fake-robot"
          ]
        }
    }
    ```
    

# Content of the MCP server

## Tools

- `setTTSLanguage`: Change the language of Nao text to speech
- `say`: Make Nao say something
- `wakeUp`: Enable Nao motors for action
- `rest`: Disable Nao motors
- `standUp`: Make Nao stand up
- `sitDown`: Make Nao sit down

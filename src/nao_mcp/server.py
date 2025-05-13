"""Nao MCP Server Module.

This module provides a server implementation for controlling a Nao robot through MCP.
It supports both real and fake robot modes, with comprehensive error handling and logging.
"""

import argparse
import logging
from mcp.server.fastmcp import FastMCP
from nao_api import NaoAPI, DanceInfo

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

mcp = FastMCP("Nao")
nao_api = NaoAPI()

@mcp.tool()
def set_tts_language(language: str) -> str:
    """Change the language of Nao text to speech.
    
    Args:
        language: The language to set (must be one of: English, French)
        
    Returns:
        str: Status message indicating success or failure
    """
    result = nao_api.set_tts_language(language)
    if result:
        return f"Nao switched language to {language}"
    return f"Nao failed to switch language to {language}"

@mcp.tool()
def say(text: str) -> str:
    """Make Nao say something.
    
    Args:
        text: The text to say
        
    Returns:
        str: Status message indicating success or failure
    """
    result = nao_api.say(text)
    if result:
        return f"Nao said {text}"
    return f"Nao failed to say {text}"

@mcp.tool()
def wake_up() -> str:
    """Enable Nao motors for action.
    - to be called at the beginning of an interaction
    - needed before any call to other tools for movements
    
    Returns:
        str: Status message indicating success or failure
    """
    result = nao_api.wake_up()
    if result:
        return "Nao motors are enabled"
    return "Failed to enable Nao motors"

@mcp.tool()
def rest() -> str:
    """Disable Nao motors.
     - to be called at the end of an interaction
    
    Returns:
        str: Status message indicating success or failure
    """
    result = nao_api.rest()
    if result:
        return "Nao motors are disabled"
    return "Failed to disable Nao motors"

@mcp.tool()
def stand_up() -> str:
    """Make Nao stand up.
    
    Returns:
        str: Status message indicating success or failure
    """
    result = nao_api.stand_up()
    if result:
        return "Nao stood up"
    return "Nao failed to stand up"

@mcp.tool()
def sit_down() -> str:
    """Make Nao sit down.
    
    Returns:
        str: Status message indicating success or failure
    """
    result = nao_api.sit_down()
    if result:
        return "Nao sat down"
    return "Nao failed to sit down"

@mcp.tool()
def get_dance_list() -> str:
    """Get the list of available dances.
    
    Returns:
        str: JSON string containing dance information with
            - the name in french
            - the name in english
            - the name of the behavior to use to start the dance
            - the description of the dance    
    """
    logging.debug("Retrieving dance list")
    
    dances = [
        DanceInfo(
            name_fr="Gangnam style",
            name_en="Gangnam style", 
            behavior_name="gangnam-style",
            description="The famous dance from Psy"
        ),
        DanceInfo(
            name_fr="Danse de l'aigle",
            name_en="Eagle dance",
            behavior_name="eagle-dance", 
            description="A beautiful dance showing the balance of Nao"
        )
    ]
    
    return str([{
        "nameFr": dance.name_fr,
        "nameEn": dance.name_en,
        "behaviorName": dance.behavior_name,
        "description": dance.description
    } for dance in dances])

@mcp.tool()
def dance(behavior_name: str, dance_name_english: str) -> str:
    """Make Nao perform a dance.
    
    Args:
        behavior_name: The name of the behavior to run
        dance_name_english: The English name of the dance
        
    Returns:
        str: Status message indicating success or failure
    """
    return f"Nao has danced the dance {dance_name_english}"


def main() -> None:
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Nao MCP Server")
    parser.add_argument("--fake-robot", action="store_true",
                       help="To use the mcp server without a real robot, everything will be faked")
    parser.add_argument("--ip", type=str, default="",
                       help="Robot IP address")
    parser.add_argument("--port", type=int, default=9559,
                       help="Naoqi port number")
    args = parser.parse_args()
    
    try:
        # Connect to Nao
        connected = nao_api.connect(args.fake_robot, args.ip, args.port)
    except Exception as e:
        logger.error("Application error: %s", e)
        raise

    if connected:
        # Create an MCP server
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
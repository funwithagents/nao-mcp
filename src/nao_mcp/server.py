import argparse
import logging
from mcp.server.fastmcp import FastMCP

class NaoAPI():

    NOT_CONNECTED_LOG = "Not connected to Nao"

    def connect(self, fake_robot: bool, ip: str = "", port: int = 0) -> bool:
        self.connected = False

        self.fake_robot = fake_robot
        if (self.fake_robot):
            logging.info("using a fake robot")
            return True

        try:
            import qi
        except ImportError:
            logging.error("could not import import qi, will act as if nao is fake_robot")
            self.fake_robot = True
            return True

        if (ip == "" or port == 0):
            logging.error("not a fake robot but ip or port is not set")
            return False

        for x in range(0, 3):
            try:
                connection_url = "tcp://" + ip + ":" + str(args.port)
                self.app = qi.Application(["SoundProcessingModule", "--qi-url=" + connection_url])
                self.app = qi.Application()
                self.app.start()
                self.connected = True
                break
            except Exception as e:
                logging.info("failed to start qi app, with error: %s", e)

        if (not self.connected):
            return False

        self.memory = self.app.session.service("ALMemory")
        self.autonomouslife = self.app.session.service("ALAutonomousLife")
        self.behaviormanager = self.app.session.service("ALBehaviorManager")
        self.motion = self.app.session.service("ALMotion")
        self.robotposture = self.app.session.service("ALRobotPosture")
        self.leds = self.app.session.service("ALLeds")
        self.tts = self.app.session.service("ALTextToSpeech")
        self.animatedspeech = self.app.session.service("ALAnimatedSpeech")
        self.basicawareness = self.app.session.service("ALBasicAwareness")

    def setTTSLanguage(self, language: str) -> bool:
        logging.debug("language = %s", language)
        
        if (self.fake_robot):
            return True
        if (not self.connected):
            logging.error(self.NOT_CONNECTED_LOG)
            return False
        
        self.tts.setLanguage(language)
        return True

    def say(self, text: str) -> bool:
        logging.debug("text = %s", text)
        
        if (self.fake_robot):
            return True
        if (not self.connected):
            logging.error(self.NOT_CONNECTED_LOG)
            return False
        
        self.animatedspeech.say(text)
        return True

    def wakeUp(self) -> bool:
        logging.debug("waking up")
        
        if (self.fake_robot):
            return True
        if (not self.connected):
            logging.error(self.NOT_CONNECTED_LOG)
            return False
        
        self.motion.wakeUp()
        return True

    def rest(self) -> bool:
        logging.debug("going to rest")
        
        if (self.fake_robot):
            return True
        if (not self.connected):
            logging.error(self.NOT_CONNECTED_LOG)
            return False
        
        self.motion.rest()
        return True

    def standUp(self) -> bool:
        """Make Nao stand up"""
        logging.debug("standing up")
        
        if (self.fake_robot):
            return True
        if (not self.connected):
            logging.error(self.NOT_CONNECTED_LOG)
            return False
        
        self.robotposture.setMaxTryNumber(3)
        result = self.robotposture.goToPosture("Stand", 0.8)
        return result

    def sitDown(self) -> bool:
        logging.debug("sitting down")

        if (self.fake_robot):
            return True
        if (not self.connected):
            logging.error(self.NOT_CONNECTED_LOG)
            return False
        
        self.robotposture.setMaxTryNumber(3)
        result = self.robotposture.goToPosture("Sit", 0.8)
        return result

    def setBasicAwarenessState(self, enabled: bool, engagementMode: str, trackingMode: str) -> bool:
        logging.debug("enabled = %s, engagementMode = %s, trackingMode %s", str(enabled), engagementMode, trackingMode)
        
        if (self.fake_robot):
            return True
        if (not self.connected):
            logging.error(self.NOT_CONNECTED_LOG)
            return False
        
        self.basicawareness.setEngagementMode(engagementMode)
        self.basicawareness.setTrackingMode(trackingMode)
        if (enabled):
            self.basicawareness.startAwareness()
        else:
            self.basicawareness.stopAwareness()
        return True

    def setBreathingEnabled(self, enabled: bool, chainName: str) -> bool:
        logging.debug("enabled = %s, chainName = %s", str(enabled), chainName)
        
        if (self.fake_robot):
            return True
        if (not self.connected):
            logging.error(self.NOT_CONNECTED_LOG)
            return False
        
        self.motion.setBreathEnabled(chainName, True)
        return True

    def runBehavior(self, behaviorName: str) -> bool:
        logging.debug("name = %s", behaviorName)
        
        if (self.fake_robot):
            return True
        if (not self.connected):
            logging.error(self.NOT_CONNECTED_LOG)
            return False
        
        self.behaviormanager.runBehavior(behaviorName)
        return True

    def stopBehavior(self, behaviorName: str) -> bool:
        logging.debug("name = %s", behaviorName)
        
        if (self.fake_robot):
            return True
        if (not self.connected):
            logging.error(self.NOT_CONNECTED_LOG)
            return False
        
        self.behaviormanager.stopBehavior(behaviorName)
        return True


# Create an MCP server
mcp = FastMCP("Nao")

@mcp.tool()
def setTTSLanguage(language: str) -> str:
    """
    Change the language of Nao text to speech
    Possible values are French or English
    """
    
    result = naoAPI.setTTSLanguage(language)
    if (result):
        return "Nao switched language to " + language
    else:
        return "Nao failed to switch language to " + language

current_tts_ids = []

@mcp.tool()
def say(text: str) -> str:
    """Make Nao say something"""

    result = naoAPI.say(text)
    if (result):
        return "Nao said " + text 
    else:
        return "Nao failed to say " + text

@mcp.tool()
def wakeUp() -> str:
    """Enable Nao motors for action - to be called at the beginning of an interaction - needed before any call to other tools for movements"""
    
    result = naoAPI.wakeUp()
    if (result):
        return "Nao motors are enabled"
    else:
        return "Failed to enable Nao motors"

@mcp.tool()
def rest() -> str:
    """Disable Nao motors - to be called at the end of an interaction"""

    result = naoAPI.rest()
    if (result):
        return "Nao motors are disabled"
    else:
        return "Failed to disable Nao motors"

@mcp.tool()
def standUp() -> str:
    """Make Nao stand up"""

    result = naoAPI.standUp()
    if (result):
        return "Nao stood up"
    else:
        return "Nao failed to stand up"

@mcp.tool()
def sitDown() -> str:
    """Make Nao sit down"""
    logging.debug("sitting down")

    result = naoAPI.sitDown()
    if (result):
        return "Nao sat down"
    else:
        return "Nao failed to sat down"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fake-robot", action='store_true',
                        help="To use the mcp server without a real robot, everything will be faked")
    parser.add_argument("--ip", type=str, default="",
                        help="Robot IP address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    args = parser.parse_args()
    global naoAPI
    naoAPI = NaoAPI()
    naoAPI.connect(args.fake_robot, args.ip, args.port)

    # Initialize and run the server
    mcp.run(transport='stdio')
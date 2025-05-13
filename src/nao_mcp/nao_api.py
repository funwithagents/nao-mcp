"""Nao API Module.

This module provides an API for interacting with a Nao robot.
It supports both real and fake robot modes, with comprehensive error handling and logging.
"""

import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NaoError(Exception):
    """Base exception for Nao-related errors."""
    pass

class ConnectionError(NaoError):
    """Exception raised when connection to the robot fails."""
    pass

class ServiceError(NaoError):
    """Exception raised when a robot service operation fails."""
    pass

@dataclass
class DanceInfo:
    """Information about a dance."""
    name_fr: str
    name_en: str
    behavior_name: str
    description: str

class NaoAPI:
    """API for interacting with a Nao robot.
    
    This class provides methods to control various aspects of the Nao robot,
    including speech, movement, and behaviors. It can operate in both real
    and fake robot modes.
    """

    NOT_CONNECTED_MESSAGE = "Not connected to Nao"
    SUPPORTED_LANGUAGES = {"English", "French"}

    # Constants
    POSTURE_SPEED = 0.8
    POSTURE_MAX_TRIES = 3

    def __init__(self) -> None:
        """Initialize the NaoAPI instance."""
        self.connected = False
        self.fake_robot = False
        self.app = None
        self.memory = None
        self.autonomous_life = None
        self.behavior_manager = None
        self.motion = None
        self.robot_posture = None
        self.leds = None
        self.tts = None
        self.animated_speech = None
        self.basic_awareness = None

    def connect(self, fake_robot: bool, ip: str = "", port: int = 0) -> bool:
        """Connect to the Nao robot.
        
        Args:
            fake_robot: Whether to use fake robot mode
            ip: Robot IP address
            port: Robot port number
            
        Returns:
            bool: True if connection successful, False otherwise
            
        Raises:
            ConnectionError: If connection fails and not in fake mode
        """
        self.connected = False
        self.fake_robot = fake_robot

        if self.fake_robot:
            logger.info("Using a fake robot")
            return True

        try:
            import qi
        except ImportError:
            logger.error("Could not import qi, will act as if nao is in fake robot mode")
            self.fake_robot = True
            return True

        if not ip or port == 0:
            error_msg = "Not a fake robot but ip or port is not set"
            logger.error(error_msg)
            raise ConnectionError(error_msg)

        try:
            connection_url = f"tcp://{ip}:{port}"
            self.app = qi.Application(["NaoAPI", f"--qi-url={connection_url}"])
            self.app.start()
            self.connected = True
            logger.info("Successfully connected to Nao robot")
        except Exception as e:
            error_msg = f"Failed to connect to Nao robot : {e}"
            logger.error(error_msg)
            raise ConnectionError(error_msg)

        if not self.connected:
            return False

        try:
            # Initialize services
            self._initialize_services()
            return True
        except Exception as e:
            error_msg = f"Failed to initialize services: {e}"
            logger.error(error_msg)
            raise ServiceError(error_msg)

    def _initialize_services(self) -> None:
        """Initialize all Nao services.
        
        Raises:
            ServiceError: If service initialization fails
        """
        try:
            self.memory = self.app.session.service("ALMemory")
            self.autonomous_life = self.app.session.service("ALAutonomousLife")
            self.behavior_manager = self.app.session.service("ALBehaviorManager")
            self.motion = self.app.session.service("ALMotion")
            self.robot_posture = self.app.session.service("ALRobotPosture")
            self.leds = self.app.session.service("ALLeds")
            self.tts = self.app.session.service("ALTextToSpeech")
            self.animated_speech = self.app.session.service("ALAnimatedSpeech")
            self.basic_awareness = self.app.session.service("ALBasicAwareness")
            logger.debug("All services initialized successfully")
        except Exception as e:
            raise ServiceError(f"Failed to initialize services: {e}")

    def _check_connection_for_return(self) -> tuple[bool, bool]:
        """Check if the robot is connected.
        
        Returns:
            tuple[bool, bool]: (True if should return, False otherwise, True if fake robot, False otherwise)
        """
        if self.fake_robot:
            return (True, True)
        if not self.connected:
            logger.error(self.NOT_CONNECTED_MESSAGE)
            return (True, False)
        return (False, False)

    def set_tts_language(self, language: str) -> bool:
        """Set the text-to-speech language.
        
        Args:
            language: The language to set (e.g., 'English', 'French')
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            ValueError: If language is not supported
        """
        logger.debug("Setting TTS language to %s", language)
        
        should_return, result = self._check_connection_for_return()
        if should_return:
            return result
        
        try:
            self.tts.setLanguage(language)
            logger.info("Successfully set TTS language to %s", language)
            return True
        except Exception as e:
            logger.error("Failed to set TTS language: %s", e)
            return False

    def say(self, text: str) -> bool:
        """Make the robot say something.
        
        Args:
            text: The text to say
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug("Saying: %s", text)
        
        should_return, result = self._check_connection_for_return()
        if should_return:
            return result
        
        try:
            self.animated_speech.say(text)
            logger.info("Successfully said: %s", text)
            return True
        except Exception as e:
            logger.error("Failed to say text: %s", e)
            return False

    def wake_up(self) -> bool:
        """Enable robot motors for action.
        
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug("Waking up robot")
        
        should_return, result = self._check_connection_for_return()
        if should_return:
            return result
        
        try:
            self.motion.wakeUp()
            logger.info("Robot successfully woke up")
            return True
        except Exception as e:
            logger.error("Failed to wake up robot: %s", e)
            return False

    def rest(self) -> bool:
        """Disable robot motors.
        
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug("Putting robot to rest")
        
        should_return, result = self._check_connection_for_return()
        if should_return:
            return result
        
        try:
            self.motion.rest()
            logger.info("Robot successfully put to rest")
            return True
        except Exception as e:
            logger.error("Failed to put robot to rest: %s", e)
            return False

    def stand_up(self) -> bool:
        """Make the robot stand up.
        
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug("Making robot stand up")
        
        should_return, result = self._check_connection_for_return()
        if should_return:
            return result
        
        try:
            self.robot_posture.setMaxTryNumber(POSTURE_MAX_TRIES)
            result = self.robot_posture.goToPosture("Stand", POSTURE_SPEED)
            if result:
                logger.info("Robot successfully stood up")
            else:
                logger.warning("Robot failed to stand up")
            return result
        except Exception as e:
            logger.error("Failed to make robot stand up: %s", e)
            return False

    def sit_down(self) -> bool:
        """Make the robot sit down.
        
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug("Making robot sit down")

        should_return, result = self._check_connection_for_return()
        if should_return:
            return result
        
        try:
            self.robot_posture.setMaxTryNumber(POSTURE_MAX_TRIES)
            result = self.robot_posture.goToPosture("Sit", POSTURE_SPEED)
            if result:
                logger.info("Robot successfully sat down")
            else:
                logger.warning("Robot failed to sit down")
            return result
        except Exception as e:
            logger.error("Failed to make robot sit down: %s", e)
            return False

    def set_basic_awareness_state(self, enabled: bool, engagement_mode: str, tracking_mode: str) -> bool:
        """Set the basic awareness state of the robot.
        
        Args:
            enabled: Whether to enable basic awareness
            engagement_mode: The engagement mode to use
            tracking_mode: The tracking mode to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug("Setting basic awareness state: enabled=%s, engagement_mode=%s, tracking_mode=%s",
                    enabled, engagement_mode, tracking_mode)
        
        should_return, result = self._check_connection_for_return()
        if should_return:
            return result
        
        try:
            self.basic_awareness.setEngagementMode(engagement_mode)
            self.basic_awareness.setTrackingMode(tracking_mode)
            if enabled:
                self.basic_awareness.startAwareness()
                logger.info("Basic awareness enabled")
            else:
                self.basic_awareness.stopAwareness()
                logger.info("Basic awareness disabled")
            return True
        except Exception as e:
            logger.error("Failed to set basic awareness state: %s", e)
            return False

    def set_breathing_enabled(self, enabled: bool, chain_name: str) -> bool:
        """Enable or disable breathing for a specific chain.
        
        Args:
            enabled: Whether to enable breathing
            chain_name: The name of the chain to control
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug("Setting breathing state: enabled=%s, chain_name=%s", enabled, chain_name)
        
        should_return, result = self._check_connection_for_return()
        if should_return:
            return result
        
        try:
            self.motion.setBreathEnabled(chain_name, enabled)
            logger.info("Successfully set breathing state for chain %s to %s", chain_name, enabled)
            return True
        except Exception as e:
            logger.error("Failed to set breathing state: %s", e)
            return False

    def run_behavior(self, behavior_name: str) -> bool:
        """Run a specific behavior.
        
        Args:
            behavior_name: The name of the behavior to run
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug("Running behavior: %s", behavior_name)
        
        should_return, result = self._check_connection_for_return()
        if should_return:
            return result
        
        try:
            self.behavior_manager.runBehavior(behavior_name)
            logger.info("Successfully started behavior: %s", behavior_name)
            return True
        except Exception as e:
            logger.error("Failed to run behavior: %s", e)
            return False

    def stop_behavior(self, behavior_name: str) -> bool:
        """Stop a running behavior.
        
        Args:
            behavior_name: The name of the behavior to stop
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug("Stopping behavior: %s", behavior_name)
        
        should_return, result = self._check_connection_for_return()
        if should_return:
            return result
        
        try:
            self.behavior_manager.stopBehavior(behavior_name)
            logger.info("Successfully stopped behavior: %s", behavior_name)
            return True
        except Exception as e:
            logger.error("Failed to stop behavior: %s", e)
            return False 
from .errors import PoleError, PoleConnectionError, RobotCrashError
from .client import PoleClient
from .robot import Robot, RobotState
from .turtle import Turtle, TurtleState

__version__ = "1.0.0"
__all__ = [
    "PoleClient",
    "Robot",
    "RobotState",
    "Turtle",
    "TurtleState",
    "PoleError",
    "PoleConnectionError",
    "RobotCrashError",
    "robot",
    "turtle",
    "робот",
    "черепаха",
    "print_to_pole",
    "clear_pole_console",
    "set_verbose",
    "печать_в_поле",
    "очистить_консоль_поля",
]

# Default singletons for quick imports (from pypole import robot, turtle)
robot = Robot()
turtle = Turtle()

# Russian alias singletons for KuMir compatibility
робот = robot
черепаха = turtle


def set_verbose(enabled: bool = True) -> None:
    robot.verbose = enabled
    turtle.verbose = enabled


def print_to_pole(text: str) -> None:
    client = PoleClient.default()
    client.send_command({"cmd": "console_print", "text": str(text)})


def clear_pole_console() -> None:
    client = PoleClient.default()
    client.send_command({"cmd": "console_clear"})


# Russian aliases
печать_в_поле = print_to_pole
очистить_консоль_поля = clear_pole_console

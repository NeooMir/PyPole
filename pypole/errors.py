# Custom error classes for PyPole library

class PoleError(Exception):
    # Base class for all Pole runtime errors
    pass


class PoleConnectionError(PoleError):
    # Raised when IPC socket connection cannot be established
    def __init__(self, message: str = "Unable to connect to Pole. Ensure the Pole application is running."):
        super().__init__(message)


class RobotCrashError(PoleError):
    # Raised when the Robot performer collides with a wall or barrier
    def __init__(self, message: str = "Robot collision detected!", x: int = 1, y: int = 1):
        super().__init__(message)
        self.message = message
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.message} (Collision at position: x={self.x}, y={self.y})"

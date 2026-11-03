# Robot performer interface for Python (PyPole).

from typing import Optional, Dict, Any
from .client import PoleClient
from .errors import RobotCrashError


class RobotState:
    # State of the Robot on the field (position, cell paint status, walls)

    def __init__(self, data: Dict[str, Any]):
        self._data = data
        self.x: int = int(data.get("x", 1))
        self.y: int = int(data.get("y", 1))
        self.is_painted: bool = bool(data.get("is_painted", False))
        self.crashed: bool = bool(data.get("crashed", False) or data.get("status") == "crash")
        self.wall_up: bool = bool(data.get("wall_up", False))
        self.wall_down: bool = bool(data.get("wall_down", False))
        self.wall_left: bool = bool(data.get("wall_left", False))
        self.wall_right: bool = bool(data.get("wall_right", False))
        self.status: str = str(data.get("status", "ok"))
        self.message: Optional[str] = data.get("message")

    # Russian property aliases for KuMir syllabus compatibility
    @property
    def закрашено(self) -> bool:
        return self.is_painted

    @property
    def чисто(self) -> bool:
        return not self.is_painted

    @property
    def разбит(self) -> bool:
        return self.crashed

    @property
    def стена_сверху(self) -> bool:
        return self.wall_up

    @property
    def стена_снизу(self) -> bool:
        return self.wall_down

    @property
    def стена_слева(self) -> bool:
        return self.wall_left

    @property
    def стена_справа(self) -> bool:
        return self.wall_right

    @property
    def сверху_стена(self) -> bool:
        return self.wall_up

    @property
    def снизу_стена(self) -> bool:
        return self.wall_down

    @property
    def слева_стена(self) -> bool:
        return self.wall_left

    @property
    def справа_стена(self) -> bool:
        return self.wall_right

    @property
    def сверху_свободно(self) -> bool:
        return not self.wall_up

    @property
    def снизу_свободно(self) -> bool:
        return not self.wall_down

    @property
    def слева_свободно(self) -> bool:
        return not self.wall_left

    @property
    def справа_свободно(self) -> bool:
        return not self.wall_right

    def walls_summary(self) -> str:
        walls = []
        if self.wall_up:
            walls.append("↑")
        if self.wall_down:
            walls.append("↓")
        if self.wall_left:
            walls.append("←")
        if self.wall_right:
            walls.append("→")
        return "".join(walls) if walls else "none"

    def __repr__(self) -> str:
        painted_str = "✓" if self.is_painted else "·"
        crash_str = " [CRASH!]" if self.crashed else ""
        return (
            f"RobotState(pos=({self.x}, {self.y}), "
            f"painted={painted_str}, "
            f"walls={self.walls_summary()}{crash_str})"
        )

    def __str__(self) -> str:
        status_text = "CRASHED" if self.crashed else "OK"
        paint_text = "Yes" if self.is_painted else "No"
        return (
            f"[Robot] Position: ({self.x}, {self.y}) | "
            f"Painted: {paint_text} | "
            f"Walls: {self.walls_summary()} | Status: {status_text}"
        )


class Robot:
    # Robot performer client for PyCharm, VS Code, or terminal

    def __init__(self, client: Optional[PoleClient] = None, verbose: bool = True):
        self.client = client or PoleClient.default()
        self.verbose = verbose

    def _execute(self, cmd: str, label: str) -> RobotState:
        res = self.client.send_command({"cmd": cmd})
        state = RobotState(res)
        if self.verbose:
            print(f"[Pole Robot] {label:<10} -> {state}")
        if state.crashed:
            err_msg = state.message or f"Robot collided with a wall at ({state.x}, {state.y})!"
            raise RobotCrashError(err_msg, x=state.x, y=state.y)
        return state

    # --- Motion methods ---

    def up(self, steps: int = 1) -> RobotState:
        # Move robot upward by given step count
        last_state = None
        for _ in range(max(1, steps)):
            last_state = self._execute("move_up", "UP")
        return last_state  # type: ignore

    def down(self, steps: int = 1) -> RobotState:
        # Move robot downward by given step count
        last_state = None
        for _ in range(max(1, steps)):
            last_state = self._execute("move_down", "DOWN")
        return last_state  # type: ignore

    def left(self, steps: int = 1) -> RobotState:
        # Move robot leftward by given step count
        last_state = None
        for _ in range(max(1, steps)):
            last_state = self._execute("move_left", "LEFT")
        return last_state  # type: ignore

    def right(self, steps: int = 1) -> RobotState:
        # Move robot rightward by given step count
        last_state = None
        for _ in range(max(1, steps)):
            last_state = self._execute("move_right", "RIGHT")
        return last_state  # type: ignore

    # Russian aliases for motion
    def вверх(self, steps: int = 1) -> RobotState:
        return self.up(steps)

    def вниз(self, steps: int = 1) -> RobotState:
        return self.down(steps)

    def влево(self, steps: int = 1) -> RobotState:
        return self.left(steps)

    def вправо(self, steps: int = 1) -> RobotState:
        return self.right(steps)

    # --- Action methods ---

    def paint(self) -> RobotState:
        # Paint current cell
        return self._execute("paint", "PAINT")

    def закрасить(self) -> RobotState:
        return self.paint()

    def reset(self) -> RobotState:
        # Reset performer to initial starting position
        return self._execute("reset", "RESET")

    def сброс(self) -> RobotState:
        return self.reset()

    def step_back(self) -> RobotState:
        # Undo last performed step
        return self._execute("step_back", "STEP_BACK")

    def шаг_назад(self) -> RobotState:
        return self.step_back()

    def назад(self) -> RobotState:
        return self.step_back()

    # --- Sensor and state queries ---

    def get_state(self) -> RobotState:
        # Query current position and wall sensors
        res = self.client.send_command({"cmd": "get_state"})
        return RobotState(res)

    def статус(self) -> RobotState:
        return self.get_state()

    def состояние(self) -> RobotState:
        return self.get_state()

    # Boolean checks for conditions in if/while
    def is_painted(self) -> bool:
        # Check if current cell is painted
        return self.get_state().is_painted

    def клетка_закрашена(self) -> bool:
        return self.is_painted()

    def is_clean(self) -> bool:
        # Check if current cell is clean
        return not self.is_painted()

    def клетка_чистая(self) -> bool:
        return self.is_clean()

    def wall_up(self) -> bool:
        # Check if wall exists above
        return self.get_state().wall_up

    def сверху_стена(self) -> bool:
        return self.wall_up()

    def стена_сверху(self) -> bool:
        return self.wall_up()

    def wall_down(self) -> bool:
        # Check if wall exists below
        return self.get_state().wall_down

    def снизу_стена(self) -> bool:
        return self.wall_down()

    def стена_снизу(self) -> bool:
        return self.wall_down()

    def wall_left(self) -> bool:
        # Check if wall exists to the left
        return self.get_state().wall_left

    def слева_стена(self) -> bool:
        return self.wall_left()

    def стена_слева(self) -> bool:
        return self.wall_left()

    def wall_right(self) -> bool:
        # Check if wall exists to the right
        return self.get_state().wall_right

    def справа_стена(self) -> bool:
        return self.wall_right()

    def стена_справа(self) -> bool:
        return self.wall_right()

    def free_up(self) -> bool:
        # Check if top is free of obstacles
        return not self.wall_up()

    def сверху_свободно(self) -> bool:
        return self.free_up()

    def free_down(self) -> bool:
        # Check if bottom is free of obstacles
        return not self.wall_down()

    def снизу_свободно(self) -> bool:
        return self.free_down()

    def free_left(self) -> bool:
        # Check if left is free of obstacles
        return not self.wall_left()

    def слева_свободно(self) -> bool:
        return self.free_left()

    def free_right(self) -> bool:
        # Check if right is free of obstacles
        return not self.wall_right()

    def справа_свободно(self) -> bool:
        return self.free_right()

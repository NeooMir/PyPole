# Turtle performer interface for Python (PyPole).

from typing import Optional, Dict, Any
from .client import PoleClient


class TurtleState:
    # State of the Turtle performer (coordinates, heading angle, pen status)

    def __init__(self, data: Dict[str, Any]):
        self._data = data
        self.x: float = float(data.get("x", 0.0))
        self.y: float = float(data.get("y", 0.0))
        self.angle: float = float(data.get("angle", 0.0))
        self.pen: bool = bool(data.get("pen", True))
        self.status: str = str(data.get("status", "ok"))

    @property
    def хвост_опущен(self) -> bool:
        return self.pen

    @property
    def угол(self) -> float:
        return self.angle

    def __repr__(self) -> str:
        pen_str = "pen down" if self.pen else "pen up"
        return f"TurtleState(pos=({self.x:.1f}, {self.y:.1f}), angle={self.angle:.0f}°, {pen_str})"

    def __str__(self) -> str:
        pen_str = "drawing" if self.pen else "moving"
        return f"[Turtle] Position: ({self.x:.1f}, {self.y:.1f}) | Heading: {self.angle:.0f}° | Pen: {pen_str}"


class Turtle:
    # Turtle performer client for vector drawing and geometry

    def __init__(self, client: Optional[PoleClient] = None, verbose: bool = True):
        self.client = client or PoleClient.default()
        self.verbose = verbose

    def _execute(self, payload: Dict[str, Any], label: str) -> TurtleState:
        res = self.client.send_command(payload)
        state = TurtleState(res)
        if self.verbose:
            print(f"[Pole Turtle] {label:<15} -> {state}")
        return state

    # --- Motion methods ---

    def forward(self, dist: float = 50.0) -> TurtleState:
        # Move turtle forward along its current heading
        return self._execute({"cmd": "turtle_forward", "dist": float(dist)}, f"FORWARD({dist})")

    def backward(self, dist: float = 50.0) -> TurtleState:
        # Move turtle backward
        return self._execute({"cmd": "turtle_backward", "dist": float(dist)}, f"BACKWARD({dist})")

    def left(self, angle: float = 90.0) -> TurtleState:
        # Turn turtle counter-clockwise (left) by specified degrees
        return self._execute({"cmd": "turtle_left", "angle": float(angle)}, f"LEFT({angle}°)")

    def right(self, angle: float = 90.0) -> TurtleState:
        # Turn turtle clockwise (right) by specified degrees
        return self._execute({"cmd": "turtle_right", "angle": float(angle)}, f"RIGHT({angle}°)")

    # Russian aliases
    def вперёд(self, dist: float = 50.0) -> TurtleState:
        return self.forward(dist)

    def вперед(self, dist: float = 50.0) -> TurtleState:
        return self.forward(dist)

    def шаг(self, dist: float = 50.0) -> TurtleState:
        return self.forward(dist)

    def назад(self, dist: float = 50.0) -> TurtleState:
        return self.backward(dist)

    def влево(self, angle: float = 90.0) -> TurtleState:
        return self.left(angle)

    def налево(self, angle: float = 90.0) -> TurtleState:
        return self.left(angle)

    def turn_left(self, angle: float = 90.0) -> TurtleState:
        return self.left(angle)

    def вправо(self, angle: float = 90.0) -> TurtleState:
        return self.right(angle)

    def направо(self, angle: float = 90.0) -> TurtleState:
        return self.right(angle)

    def turn_right(self, angle: float = 90.0) -> TurtleState:
        return self.right(angle)

    # --- Pen and canvas controls ---

    def pen_down(self) -> TurtleState:
        # Lower pen: turtle leaves drawing path
        return self._execute({"cmd": "turtle_pen_down"}, "PEN_DOWN")

    def pen_up(self) -> TurtleState:
        # Raise pen: turtle moves without drawing
        return self._execute({"cmd": "turtle_pen_up"}, "PEN_UP")

    def опустить_хвост(self) -> TurtleState:
        return self.pen_down()

    def опусти_хвост(self) -> TurtleState:
        return self.pen_down()

    def перо_вниз(self) -> TurtleState:
        return self.pen_down()

    def поднять_хвост(self) -> TurtleState:
        return self.pen_up()

    def подними_хвост(self) -> TurtleState:
        return self.pen_up()

    def перо_вверх(self) -> TurtleState:
        return self.pen_up()

    def clear(self) -> TurtleState:
        # Clear drawings from canvas
        return self._execute({"cmd": "turtle_clear"}, "CLEAR")

    def очистить(self) -> TurtleState:
        return self.clear()

    def очистить_холст(self) -> TurtleState:
        return self.clear()

    def home(self) -> TurtleState:
        # Return turtle to center (0, 0)
        return self._execute({"cmd": "turtle_reset"}, "HOME")

    def домой(self) -> TurtleState:
        return self.home()

    def reset(self) -> TurtleState:
        return self.home()

    def step_back(self) -> TurtleState:
        # Undo last turtle step
        return self._execute({"cmd": "turtle_step_back"}, "STEP_BACK")

    def шаг_назад(self) -> TurtleState:
        return self.step_back()

    def get_state(self) -> TurtleState:
        # Query current turtle state
        res = self.client.send_command({"cmd": "turtle_status"})
        return TurtleState(res)

    def статус(self) -> TurtleState:
        return self.get_state()

    def состояние(self) -> TurtleState:
        return self.get_state()

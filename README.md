# PyPole (neoomir-pypole)

**PyPole** (`neoomir-pypole`) is the official Python API binding and client library for the **Pole** (NeoMir) educational IDE.

It allows students and developers to write Python algorithms in their favorite IDEs (**PyCharm**, **VS Code**, **Jupyter**, or system terminal) and control the performers (**Robot** and **Turtle**) running in the Pole graphical window in real time, with instant diagnostic state streaming straight into your IDE run console.

---

## Key Features

- **Real-Time Visual Execution:** Commands execute in the Pole canvas with smooth animation, step tracking, and visual feedback.
- **Instant IDE Console Output:** Calling performer methods automatically logs formatted status updates, coordinates, and sensor metrics directly to your PyCharm / terminal console (`verbose=True` by default).
- **Flexible Import Styles:** Import via `neoomir_pypole`, `pypole`, or `pole`:
  ```python
  from neoomir_pypole import robot, turtle
  # or
  from pypole import robot, turtle
  # or
  from pole import robot, turtle
  ```
- **Full Bilingual Support:** Supports both standard English API names and Russian algorithmic keywords matching the KuMir educational syllabus:
  - `robot.right()` and `робот.вправо()`
  - `turtle.forward(100)` and `черепаха.вперёд(100)`
- **Zero Configuration:** Automatically locates Unix Domain Socket or Windows Named Pipe connections to the active Pole instance (including `NEOMIR_SOCKET` / `POLE_SOCKET` environment variables and Flatpak runtime directories).
- **Built-in Safety & Diagnostics:** Raises structured exceptions such as `RobotCrashError` when colliding with walls, with exact coordinates of the collision.

---

## Installation

### 1. From PyPI (Recommended for PyCharm / VS Code)

In your project environment or PyCharm terminal:
```bash
pip install neoomir-pypole
```

> [!IMPORTANT]
> The official PyPI package name is **`neoomir-pypole`**. Make sure to run `pip install neoomir-pypole` inside the virtual environment (`venv`) of your IDE project.

### 2. PyCharm Setup Guide

If PyCharm shows `ModuleNotFoundError: No module named 'pypole'` or `'neoomir_pypole'`:
1. **Using PyCharm Terminal**:
   Open the **Terminal** tab at the bottom of PyCharm (it automatically activates your project's `.venv`) and run:
   ```bash
   pip install neoomir-pypole
   ```
2. **Using PyCharm Settings**:
   - Go to **File → Settings** (or **Preferences** on macOS) → **Project: ... → Python Interpreter**.
   - Click the **+** (Install) button.
   - Type `neoomir-pypole` and click **Install Package**.
3. **From Local Source Directory**:
   If working directly within this repository in PyCharm, right-click the `python/` directory in the Project Explorer tree and select:
   **Mark Directory as → Sources Root**.

### 3. From Local Source (Editable Mode)

Inside the `python/` folder:
```bash
pip install -e .
```

From the repository root:
```bash
pip install -e ./python
```

---

## Quick Start in PyCharm / VS Code

### 1. Controlling the Robot (English Syntax)

```python
from neoomir_pypole import robot
# (also works: from pypole import robot)

# Reset field to starting position
robot.reset()

# Move along corridor and paint cells
while robot.free_right():
    robot.right()
    robot.paint()

# Check wall sensors
if robot.wall_up():
    print("Wall detected above the robot!")
```

### 2. Controlling the Robot (Russian Syntax / KuMir Style)

```python
from neoomir_pypole import робот
# (also works: from pypole import робот)

робот.сброс()

while робот.справа_свободно():
    робот.вправо()
    робот.закрасить()

if робот.сверху_стена():
    print("Обнаружена стена сверху!")
```

### 3. Controlling the Turtle (Vector Graphics)

```python
from neoomir_pypole import turtle
# (also works: from pypole import turtle)

turtle.home()
turtle.clear()
turtle.pen_down()

# Draw an equilateral triangle
for _ in range(3):
    turtle.forward(100)
    turtle.left(120)

print(f"Current turtle position: {turtle.get_state()}")
```

---

## Real-Time Console Output in PyCharm

When running commands from PyCharm, each step prints detailed diagnostic information directly to the Run Tool Window:

```text
[Pole Robot] RESET      -> [Робот] Позиция: (1, 1) | Закрашено: Нет | Стены: ↑← | Статус: ОК
[Pole Robot] ВПРАВО     -> [Робот] Позиция: (2, 1) | Закрашено: Нет | Стены: ↑  | Статус: ОК
[Pole Robot] ЗАКРАСИТЬ  -> [Робот] Позиция: (2, 1) | Закрашено: Да  | Стены: ↑  | Статус: ОК
[Pole Turtle] ВПЕРЁД(100) -> [Черепаха] Позиция: (100.0, 0.0) | Угол: 90° | Перо: рисует
```

To mute automatic console printing, pass `verbose=False` or call `set_verbose(False)`:
```python
from neoomir_pypole import robot, set_verbose

set_verbose(False)
robot.right(5)  # Executes silently in Pole without printing to IDE console
```

---

## API Reference

### Robot Performer (`neoomir_pypole.Robot`)

| Method (EN) | Method (RU) | Description |
| :--- | :--- | :--- |
| `robot.up(n=1)` | `робот.вверх(n=1)` | Move up by *n* cells |
| `robot.down(n=1)` | `робот.вниз(n=1)` | Move down by *n* cells |
| `robot.left(n=1)` | `робот.влево(n=1)` | Move left by *n* cells |
| `robot.right(n=1)` | `робот.вправо(n=1)` | Move right by *n* cells |
| `robot.paint()` | `робот.закрасить()` | Paint current cell |
| `robot.reset()` | `робот.сброс()` | Reset performer to starting point |
| `robot.step_back()` | `робот.шаг_назад()` | Undo last action |
| `robot.get_state()` | `робот.состояние()` | Returns `RobotState` object |
| `robot.wall_up()` | `робот.стена_сверху()` | `True` if obstacle above |
| `robot.wall_down()` | `робот.стена_снизу()` | `True` if obstacle below |
| `robot.wall_left()` | `робот.стена_слева()` | `True` if obstacle to the left |
| `robot.wall_right()` | `робот.стена_справа()` | `True` if obstacle to the right |
| `robot.free_up()` | `робот.сверху_свободно()` | `True` if upward direction is open |
| `robot.free_down()` | `робот.снизу_свободно()` | `True` if downward direction is open |
| `robot.free_left()` | `робот.слева_свободно()` | `True` if left direction is open |
| `robot.free_right()` | `робот.справа_свободно()` | `True` if right direction is open |
| `robot.is_painted()` | `робот.клетка_закрашена()` | `True` if current cell is painted |
| `robot.is_clean()` | `робот.клетка_чистая()` | `True` if current cell is clean |

### Turtle Performer (`neoomir_pypole.Turtle`)

| Method (EN) | Method (RU) | Description |
| :--- | :--- | :--- |
| `turtle.forward(d=50)` | `черепаха.вперёд(d=50)` | Move forward along heading |
| `turtle.backward(d=50)` | `черепаха.назад(d=50)` | Move backward |
| `turtle.left(a=90)` | `черепаха.влево(a=90)` | Turn counter-clockwise by *a* degrees |
| `turtle.right(a=90)` | `черепаха.вправо(a=90)` | Turn clockwise by *a* degrees |
| `turtle.pen_down()` | `черепаха.опустить_хвост()` | Lower pen (draw path) |
| `turtle.pen_up()` | `черепаха.поднять_хвост()` | Raise pen (move without drawing) |
| `turtle.home()` | `черепаха.домой()` | Return to center (0, 0) |
| `turtle.clear()` | `черепаха.очистить()` | Clear canvas drawings |
| `turtle.step_back()` | `черепаха.шаг_назад()` | Undo last turtle step |

---

## Exception Handling

```python
from neoomir_pypole import robot, RobotCrashError, PoleConnectionError

try:
    robot.up(10)
except PoleConnectionError as e:
    print(f"Pole application is not running: {e}")
except RobotCrashError as e:
    print(f"Robot crashed into wall at ({e.x}, {e.y})!")
```

---

## License

MIT License. Part of the **Pole (NeoMir)** educational platform.

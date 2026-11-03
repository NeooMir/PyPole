#!/usr/bin/env python3
"""
Demonstration script for PyCharm, VS Code, or terminal.
Controls Robot and Turtle performers in the running Pole IDE.
Step-by-step execution results are automatically streamed to the PyCharm run console!
"""

import sys
import os

# Add parent directory to sys.path if pypole is not installed via pip
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pypole import robot, turtle, print_to_pole, clear_pole_console, RobotCrashError, PoleConnectionError

def main():
    print("=== PyPole Client Demonstration ===")
    
    try:
        # Send greeting to the Pole IDE console window
        print_to_pole("External script connected via PyPole!")
        
        print("\n--- 1. Robot Control ---")
        # Reset robot to starting position
        robot.reset()
        
        # Step right and paint cells
        robot.right(2)
        robot.paint()
        robot.down()
        robot.paint()
        
        # Check wall and cell sensors
        print(f"Wall above: {robot.wall_up()}")
        print(f"Free to the right: {robot.free_right()}")
        print(f"Current cell painted: {robot.is_painted()}")
        
        print("\n--- 2. Turtle Control ---")
        turtle.home()
        turtle.clear()
        
        # Draw an equilateral triangle
        print("Drawing triangle with Turtle...")
        for _ in range(3):
            turtle.forward(80)
            turtle.left(120)
            
        print("\nFinished! Results displayed in Pole window and streamed to PyCharm console.")

    except PoleConnectionError as e:
        print(f"\n[Connection Error]: {e}")
        print("Hint: Launch the Pole (NeoMir) application so the script can connect via IPC socket.")
    except RobotCrashError as e:
        print(f"\n[Robot Collision]: {e}")
    except Exception as e:
        print(f"\n[Unexpected Error]: {e}")

if __name__ == "__main__":
    main()

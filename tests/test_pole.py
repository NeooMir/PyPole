"""Unit tests for the PyPole Python API library."""

import unittest
from pypole import Robot, Turtle, RobotState, TurtleState, PoleConnectionError, RobotCrashError
import pole  # compatibility alias test


class MockClient:
    def __init__(self):
        self.history = []
        self.next_response = None

    def send_command(self, payload):
        self.history.append(payload)
        if self.next_response:
            resp = self.next_response
            self.next_response = None
            return resp
        cmd = payload.get("cmd")
        if cmd == "move_up":
            return {"status": "ok", "x": 1, "y": 2, "is_painted": False, "crashed": False}
        elif cmd == "move_down":
            return {"status": "ok", "x": 1, "y": 1, "is_painted": False, "crashed": False}
        elif cmd == "move_left":
            return {"status": "ok", "x": 1, "y": 1, "is_painted": False, "crashed": False}
        elif cmd == "move_right":
            return {"status": "ok", "x": 2, "y": 1, "is_painted": False, "crashed": False}
        elif cmd == "paint":
            return {"status": "ok", "x": 2, "y": 1, "is_painted": True, "crashed": False}
        elif cmd == "turtle_forward":
            return {"status": "ok", "x": 50.0, "y": 0.0, "angle": 90.0, "pen": True}
        elif cmd == "turtle_left":
            return {"status": "ok", "x": 0.0, "y": 0.0, "angle": 180.0, "pen": True}
        return {"status": "ok", "x": 1, "y": 1, "is_painted": False, "crashed": False, "wall_up": False, "wall_right": False}


class TestPyPoleApi(unittest.TestCase):
    def test_package_aliases(self):
        self.assertIsNotNone(pole.Robot)
        self.assertIsNotNone(pole.Turtle)

    def test_robot_state_properties(self):
        st = RobotState({
            "status": "ok",
            "x": 4,
            "y": 5,
            "is_painted": True,
            "crashed": False,
            "wall_up": True,
            "wall_down": False,
            "wall_left": False,
            "wall_right": True
        })
        self.assertEqual(st.x, 4)
        self.assertEqual(st.y, 5)
        self.assertTrue(st.is_painted)
        self.assertTrue(st.закрашено)
        self.assertFalse(st.чисто)
        self.assertTrue(st.стена_сверху)
        self.assertTrue(st.сверху_стена)
        self.assertFalse(st.сверху_свободно)
        self.assertTrue(st.снизу_свободно)
        self.assertTrue(st.слева_свободно)
        self.assertFalse(st.справа_свободно)

    def test_robot_methods(self):
        client = MockClient()
        bot = Robot(client=client, verbose=False)

        bot.right()
        self.assertEqual(client.history[-1], {"cmd": "move_right"})

        bot.вправо()
        self.assertEqual(client.history[-1], {"cmd": "move_right"})

        bot.paint()
        self.assertEqual(client.history[-1], {"cmd": "paint"})

        bot.закрасить()
        self.assertEqual(client.history[-1], {"cmd": "paint"})

    def test_robot_crash_raises(self):
        client = MockClient()
        client.next_response = {
            "status": "crash",
            "x": 1,
            "y": 1,
            "crashed": True,
            "wall_up": True,
            "message": "Wall collision error!"
        }
        bot = Robot(client=client, verbose=False)
        with self.assertRaises(RobotCrashError) as ctx:
            bot.up()
        self.assertIn("Wall collision", str(ctx.exception))

    def test_turtle_methods(self):
        client = MockClient()
        turtle = Turtle(client=client, verbose=False)

        turtle.forward(50)
        self.assertEqual(client.history[-1], {"cmd": "turtle_forward", "dist": 50.0})

        turtle.вперёд(100)
        self.assertEqual(client.history[-1], {"cmd": "turtle_forward", "dist": 100.0})

        turtle.left(90)
        self.assertEqual(client.history[-1], {"cmd": "turtle_left", "angle": 90.0})

        turtle.опустить_хвост()
        self.assertEqual(client.history[-1], {"cmd": "turtle_pen_down"})

        turtle.поднять_хвост()
        self.assertEqual(client.history[-1], {"cmd": "turtle_pen_up"})


if __name__ == "__main__":
    unittest.main()

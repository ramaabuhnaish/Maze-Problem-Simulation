########################################################################################################################################
                                                                 # API.py File #                                                    
"""
This script provides a Python interface to control a simulated maze-solving robot. It defines a set of utility functions 
to interact with the simulator by sending commands via standard input/output. The primary features include:

1. Command Communication:
   - The `command` function sends instructions to the simulator and optionally processes responses based on the specified return type.

2. Maze Information:
   - Functions like `mazeWidth()` and `mazeHeight()` retrieve the dimensions of the maze.

3. Wall Detection:
   - Functions such as `wallFront()`, `wallBack()`, `wallLeft()`, and `wallRight()` check for walls in specific directions. 
   - Extended checks are available for diagonal directions like `wallFrontLeft()` and `wallBackRight()`.

4. Movement and Rotation:
   - The robot can move using `moveForward()` or `moveForwardHalf()`.
   - Rotation is supported via functions like `turnRight()`, `turnLeft()`, `turnRight90()`, and `turnLeft45()`.

5. Maze Customization:
   - Functions such as `setWall()`, `clearWall()`, and `setColor()` allow the user to modify the maze dynamically by adding or removing walls and setting colors.

6. Text Annotations:
   - Functions like `setText()` and `clearText()` enable placing and removing text annotations within the maze.

7. State Management:
   - The script includes methods to check and acknowledge simulator resets (`wasReset()` and `ackReset()`).

8. Error Handling:
   - A custom exception, `MouseCrashedError`, is raised when the robot crashes while moving.

This modular design makes it easier to control the maze-solving robot and customize the maze environment programmatically.
"""

########################################################################################################################################

import sys

class MouseCrashedError(Exception):
    pass

def command(args, return_type=None):
    line = " ".join([str(x) for x in args]) + "\n"
    sys.stdout.write(line)
    sys.stdout.flush()
    if return_type:
        response = sys.stdin.readline().strip()
        if return_type == bool:
            return response == "true"
        return return_type(response)

def mazeWidth():
    return command(args=["mazeWidth"], return_type=int)

def mazeHeight():
    return command(args=["mazeHeight"], return_type=int)

def checkWall(wallCommand, half_steps_away=None):
    args = [wallCommand]
    if half_steps_away is not None:
        args.append(half_steps_away)
    return command(args, return_type=bool)

def wallFront(half_steps_away=None):
    return checkWall("wallFront", half_steps_away)

def wallBack(half_steps_away=None):
    return checkWall("wallBack", half_steps_away)

def wallLeft(half_steps_away=None):
    return checkWall("wallLeft", half_steps_away)

def wallRight(half_steps_away=None):
    return checkWall("wallRight", half_steps_away)

def wallFrontLeft(half_steps_away=None):
    return checkWall("wallFrontLeft", half_steps_away)

def wallFrontRight(half_steps_away=None):
    return checkWall("wallFrontRight", half_steps_away)

def wallBackLeft(half_steps_away=None):
    return checkWall("wallBackLeft", half_steps_away)

def wallBackRight(half_steps_away=None):
    return checkWall("wallBackRight", half_steps_away)

def moveForward(distance=None):
    args = ["moveForward"]
    # Don't append distance argument unless explicitly specified, for
    # backwards compatibility with older versions of the simulator
    if distance is not None:
        args.append(distance)
    response = command(args=args, return_type=str)
    if response == "crash":
        raise MouseCrashedError()

def moveForwardHalf(num_half_steps=None):
    args = ["moveForwardHalf"]
    if num_half_steps is not None:
        args.append(num_half_steps)
    response = command(args=args, return_type=str)
    if response == "crash":
        raise MouseCrashedError()

def turnRight():
    command(args=["turnRight"], return_type=str)

def turnLeft():
    command(args=["turnLeft"], return_type=str)

def turnRight90():
    turnRight()

def turnLeft90():
    turnLeft()

def turnRight45():
    command(args=["turnRight45"], return_type=str)

def turnLeft45():
    command(args=["turnLeft45"], return_type=str)

def setWall(x, y, direction):
    command(args=["setWall", x, y, direction])

def clearWall(x, y, direction):
    command(args=["clearWall", x, y, direction])

def setColor(x, y, color):
    command(args=["setColor", x, y, color])

def clearColor(x, y):
    command(args=["clearColor", x, y])

def clearAllColor():
    command(args=["clearAllColor"])

def setText(x, y, text):
    command(args=["setText", x, y, text])

def clearText(x, y):
    command(args=["clearText", x, y])

def clearAllText():
    command(args=["clearAllText"])

def wasReset():
    return command(args=["wasReset"], return_type=bool)

def ackReset():
    command(args=["ackReset"], return_type=str)
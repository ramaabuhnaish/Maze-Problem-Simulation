########################################################################################################################################
                                                           # Right Hand Rule File #                                                    

"""
This script controls a maze-solving mouse simulator, which navigates the maze using the right-hand rule algorithm. 
Key functionalities and structure:

1. Initialization:
   - The mouse starts at position `(0, 0)` facing north (`cur_direction = 0`).
   - The goal positions are predefined (e.g., `(12, 7)`).

2. Logging and Debugging:
   - `log_message()` outputs messages to standard error for debugging purposes.
   - Functions like `print_int()` and `print_pos()` log the mouse's position in the maze.

3. Goal Check:
   - The `check()` function determines if the mouse has reached one of the goal positions. 
   - If a goal is reached, it logs the completion time and terminates the simulation.

4. Movement and Direction Updates:
   - `update_position()` adjusts the mouse's coordinates based on its current direction.
   - `update_direction()` updates the direction when the mouse turns (left or right).

5. Maze Interaction:
   - Uses the `API` module to interact with the maze:
     - `API.wallRight()`, `API.wallFront()`, and `API.wallLeft()` check for walls around the mouse.
     - `API.moveForward()` moves the mouse forward.
     - `API.turnRight()` and `API.turnLeft()` change the mouse's direction.
     - `API.setColor()` and `API.setText()` mark visited cells and display text.

6. Right-Hand Rule Algorithm:
   - The mouse always tries to keep its right side against a wall.
   - If the right wall is present, it checks the front and left directions:
     - Moves forward if there's no wall in front.
     - Turns left and moves if there's a wall in front but none to the left.
     - Turns around and moves forward if walls surround it.
   - If there's no right wall, the mouse turns right and moves forward.

7. Goal Reaching and Termination:
   - The script continually checks if the mouse has reached the goal.
   - Once a goal is reached, the elapsed time is logged, and the program terminates.

8. Main Function:
   - Initializes the maze by marking the start and goal positions.
   - Continuously executes the right-hand rule algorithm until the goal is reached.

This script integrates logical navigation with real-time maze interaction, ensuring efficient traversal and debugging support.
"""

########################################################################################################################################

import sys
import time
import API

cur_direction = 0
# Current position starts from (0, 0)
x, y = 0, 0

def log_message(text):
    sys.stderr.write(text)
    sys.stderr.flush()

def print_pos(x, y):
    # Print the current position
    log_message("Position ({}, {})\n".format(x, y))

def check(x, y, goal_positions, start_time):
    if (x, y) in goal_positions:
        end_time = time.time()
        completion_time = end_time - start_time
        log_message("The mouse reached one of the goals!!\n")
        log_message("Goal reached at ({}, {})\n".format(x, y))
        log_message("Elapsed time: {:.2f} seconds\n".format(completion_time))
        return True
    return False

# Updates the position of the mouse based on the current direction
def update_position():
    global x, y
    if cur_direction == 0:  # Facing north
        y += 1
    elif cur_direction == 1:  # Facing east
        x += 1
    elif cur_direction == 2:  # Facing south
        y -= 1
    elif cur_direction == 3:  # Facing west
        x -= 1

# This function takes -1 if turned to left, 1 if turned to right
def update_direction(turn_difriction):
    global cur_direction
    cur_direction = (cur_direction + turn_difriction) % 4

def mark_as_visited():
    API.setColor(x, y, 'a')

def main():
    log_message("Running...\n")

    # Define goal positions
    goal_positions = [((API.mazeWidth())-4, (API.mazeHeight()//2)-1)]

    # Set initial and goal positions
    API.setColor(x, y, 'R')
    API.setText(x, y, "Start")

    for gx, gy in goal_positions:
        API.setColor(gx, gy, 'G')
        API.setText(gx, gy, "Goal")

    log_message("Colors were set...\n")

    start_time = time.time()

    while True:
        if check(x, y, goal_positions, start_time):
            return

        # Follow the right wall
        while API.wallRight():
            if check(x, y, goal_positions, start_time):
                return

            log_message("Wall on the right\n")
            if not API.wallFront():
                # If there's no wall in front, move forward
                mark_as_visited()
                API.moveForward()
                update_position()
                print_pos(x, y)
                log_message("Moved one step forward\n")
            else:
                # If there is a wall in front
                if not API.wallLeft():
                    log_message("Wall in front\n")
                    log_message("No wall on the left\n")
                    API.turnLeft()
                    update_direction(-1)
                    log_message("Turned to the left\n")
                    mark_as_visited()
                    API.moveForward()
                    update_position()
                    print_pos(x, y)
                    log_message("Moved forward\n")
                else:
                    # If there are walls in all directions
                    # Turn around and move forward
                    API.turnLeft()
                    update_direction(-1)
                    API.turnLeft()
                    update_direction(-1)
                    log_message("Turned around\n")
                    mark_as_visited()
                    API.moveForward()
                    update_position()
                    print_pos(x, y)
                    log_message("Moved forward\n")

        if check(x, y, goal_positions, start_time):
            return

        # Turn right if there's no wall on the right
        API.turnRight()
        update_direction(1)
        log_message(f"cur_direction = {cur_direction}\n")
        mark_as_visited()
        API.moveForward()
        update_position()
        print_pos(x, y)

if __name__ == "__main__":
    main()

########################################################################################################################################
                                                           # Left Hand Rule File #                                                    

"""
This script controls a robot to navigate through a maze using a left-wall-following algorithm. Key components and functionality include:

1. Starting Position:
   - The robot starts at position `(0, 0)` with the direction facing north (0).
   - The goal is set at `(12, 7)`.

2. Direction and Position Management:
   - `cur_direction` keeps track of the robot's current facing direction:
     - `0`: North
     - `1`: East
     - `2`: South
     - `3`: West
   - `update_position()` updates the robot's position `(x, y)` based on the direction and movement.
   - `update_direction(turn_difriction)` adjusts the robot's direction after a turn, ensuring the direction is always within valid bounds (0-3).

3. Wall Detection and Navigation:
   - The robot navigates by following the left wall using the following logic:
     - If there's a wall on the left, it checks if it can move forward.
     - If blocked ahead, it checks the right side.
     - If surrounded by walls, it turns around and continues.
   - `API.wallLeft()`, `API.wallFront()`, and `API.wallRight()` are used to detect the presence of walls.

4. Goal Detection:
   - `check()` verifies if the robot has reached one of the goal positions:
     - Logs the success and elapsed time upon reaching the goal.

5. Color Marking:
   - The starting position is marked with red (`'R'`) and labeled `"Start"`.
   - The goal position is marked with green (`'G'`) and labeled `"Goal"`.
   - Cells visited by the robot are marked with `'a'` using `API.setColor()`.

6. Main Algorithm:
   - Executes a continuous loop where the robot navigates the maze, follows the left wall, and adjusts its position until the goal is reached.

7. Improvement Suggestions:
   - Enhance the algorithm to dynamically switch between left and right wall-following based on specific maze configurations.
   - Implement a flood-fill algorithm for more efficient navigation in complex mazes.
   - Improve the logging mechanism for debugging and visualization purposes.
"""

########################################################################################################################################

import sys
import API
import time

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

        # Follow the left wall
        while API.wallLeft():
            if check(x, y, goal_positions, start_time):
                return

            log_message("Wall on the left\n")
            if not API.wallFront():
                # If there's no wall in front, move forward
                mark_as_visited()
                API.moveForward()
                update_position()
                print_pos(x, y)
                log_message("Moved one step forward\n")
            else:
                # If there is a wall in front
                if not API.wallRight():
                    log_message("Wall in front\n")
                    log_message("No wall on the right\n")
                    API.turnRight()
                    update_direction(1)
                    log_message("Turned to the right\n")
                    mark_as_visited()
                    API.moveForward()
                    update_position()
                    print_pos(x, y)
                    log_message("Moved forward\n")
                else:
                    # If there are walls in all directions
                    # Turn around and move forward
                    API.turnRight()
                    update_direction(1)
                    API.turnRight()
                    update_direction(1)
                    log_message("Turned around\n")
                    mark_as_visited()
                    API.moveForward()
                    update_position()
                    print_pos(x, y)
                    log_message("Moved forward\n")

        if check(x, y, goal_positions, start_time):
            return

        # Turn left if there's no wall on the left
        API.turnLeft()
        update_direction(-1)
        log_message(f"cur_direction = {cur_direction}\n")
        mark_as_visited()
        API.moveForward()
        update_position()
        print_pos(x, y)

if __name__ == "__main__":
    main()
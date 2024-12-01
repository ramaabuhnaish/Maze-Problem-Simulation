########################################################################################################################################
                                                     # Flood Fill Algorithm File #          
                                                                                               
"""
This script implements a flood-fill algorithm for navigating a robot through a maze simulation. It uses a grid-based representation and sensor data to detect walls and determine the optimal path to a goal. Key components and functionalities include:

1. Grid Representation:
   - The maze is represented as a grid of size `16x16` (`MAX_X` and `MAX_Y`).
   - `flood_fill_path` stores the shortest path distances to the goal, initialized with `-1`.
   - `wall_info` encodes wall information for each cell using bit flags.

2. Wall Detection and Update:
   - `fetch_sensor_data()` collects sensor readings to detect walls on the left, front, and right sides of the robot.
   - `update_wall_info()` updates the `wall_info` array based on sensor data and the robot's current orientation.

3. Flood-Fill Algorithm:
   - `flood_fill()` calculates the shortest path distances from the goal to all reachable cells using a recursive flood-fill approach.

4. Pathfinding:
   - `determine_next_move()` uses the `flood_fill_path` array and wall information to select the next direction with the lowest distance value.
   - Priority is given to cells that are closer to the goal and not blocked by walls.

5. Robot Movement:
   - `rotate_robot()` aligns the robot to the next desired direction.
   - `advance_robot()` moves the robot forward and updates its position on the grid.

6. Maze Customization:
   - Colors and text are used to visualize the maze:
     - Start position is marked with red (`R`).
     - Goal positions are marked with green (`G`).
     - Visited cells are marked with blue (`B`).

7. Goal Detection:
   - The robot stops when it reaches one of the predefined goal positions.

8. Main Function:
   - Initializes the flood-fill path and sets the start and goal positions.
   - Continuously updates the flood-fill path, determines the next move, and advances the robot until a goal is reached.
   - Logs the completion time upon reaching the goal.

This implementation combines logical navigation, real-time wall detection, and a visualization mechanism to navigate the maze effectively using the flood-fill algorithm.
"""

########################################################################################################################################

import API
import time
import sys

MAX_X = API.mazeWidth()
MAX_Y = API.mazeHeight()

# Global Variable
current_row = MAX_X - 1  # Starting at the bottom-left corner
current_col = 0

flood_fill_path = [[-1 for _ in range(MAX_Y)] for _ in range(MAX_X)]
wall_info = [[0 for _ in range(MAX_Y)] for _ in range(MAX_X)]

# Check if there is a wall in a specific direction
is_wall_left = False
is_wall_right = False
is_wall_front = False

# Robout directions:
# Let: Up = 0, Right = 1, Down = 2, Left = 3
next_direction = 1
current_direction = 0


def log_message(text):
    sys.stderr.write(text)
    sys.stderr.flush()

def initialize_flood_fill_path():
    '''Initialize flood_fill_path array to default values.'''
    global flood_fill_path
    flood_fill_path = [[-1 for _ in range(MAX_Y)] for _ in range(MAX_X)]


def flood_fill(row, col, distance):
    '''Apply Flood Fill Algorithm'''
    if row < 0 or row >= MAX_X or col < 0 or col >= MAX_Y:
        return
    if flood_fill_path[row][col] <= distance and flood_fill_path[row][col] != -1:
        return
    flood_fill_path[row][col] = distance

    if col < MAX_Y - 1 and not (wall_info[row][col] & 0b0100):
        flood_fill(row, col + 1, distance + 1)
    if col > 0 and not (wall_info[row][col - 1] & 0b0100):
        flood_fill(row, col - 1, distance + 1)
    if row < MAX_X - 1 and not (wall_info[row][col] & 0b0010):
        flood_fill(row + 1, col, distance + 1)
    if row > 0 and not (wall_info[row - 1][col] & 0b0010):
        flood_fill(row - 1, col, distance + 1)


def fetch_sensor_data():
    '''Collecting sensor data'''
    global is_wall_left, is_wall_right, is_wall_front
    is_wall_left = API.wallLeft()
    is_wall_front = API.wallFront()
    is_wall_right = API.wallRight()
    log_message("Sensor Data - Left: {}, Front: {}, Right: {}\n".format(is_wall_left, is_wall_front, is_wall_right))
    

def update_wall_info():
    '''Update wall information in the wall_info array'''
    max_index = MAX_X - 1
    if current_direction == 0:  # Facing Up
        if is_wall_left and current_col > 0:
            wall_info[current_row][current_col - 1] |= 0b0100
            API.setWall(current_col, max_index - current_row, 'w')
        if is_wall_right and current_col < max_index:
            wall_info[current_row][current_col] |= 0b0100
            API.setWall(current_col, max_index - current_row, 'e')
        if is_wall_front and current_row > 0:
            wall_info[current_row - 1][current_col] |= 0b0010
            API.setWall(current_col, max_index - current_row, 'n')
    elif current_direction == 1:  # Facing Right
        if is_wall_left and current_row > 0:
            wall_info[current_row - 1][current_col] |= 0b0010
            API.setWall(current_col, max_index - current_row, 'n')
        if is_wall_right and current_row < max_index:
            wall_info[current_row][current_col] |= 0b0010
            API.setWall(current_col, max_index - current_row, 's')
        if is_wall_front and current_col < max_index:
            wall_info[current_row][current_col] |= 0b0100
            API.setWall(current_col, max_index - current_row, 'e')
    elif current_direction == 2:  # Facing Down
        if is_wall_left and current_col < max_index:
            wall_info[current_row][current_col] |= 0b0100
            API.setWall(current_col, max_index - current_row, 'e')
        if is_wall_right and current_col > 0:
            wall_info[current_row][current_col - 1] |= 0b0100
            API.setWall(current_col, max_index - current_row, 'w')
        if is_wall_front and current_row < max_index:
            wall_info[current_row][current_col] |= 0b0010
            API.setWall(current_col, max_index - current_row, 's')
    elif current_direction == 3:  # Facing Left
        if is_wall_left and current_row < max_index:
            wall_info[current_row][current_col] |= 0b0010
            API.setWall(current_col, max_index - current_row, 's')
        if is_wall_right and current_row > 0:
            wall_info[current_row - 1][current_col] |= 0b0010
            API.setWall(current_col, max_index - current_row, 'n')
        if is_wall_front and current_col > 0:
            wall_info[current_row][current_col - 1] |= 0b0100
            API.setWall(current_col, max_index - current_row, 'w')

def determine_next_move():
    '''Determine the best direction for the robot'''
    global next_direction
    left = flood_fill_path[current_row][current_col - 1] if current_col > 0 else 99
    right = flood_fill_path[current_row][current_col + 1] if current_col < MAX_X - 1 else 99
    up = flood_fill_path[current_row - 1][current_col] if current_row > 0 else 99
    down = flood_fill_path[current_row + 1][current_col] if current_row < MAX_X - 1 else 99

    # Check walls
    if current_row > 0 and (wall_info[current_row - 1][current_col] & 0b0010):
        up = 99
    if current_col > 0 and (wall_info[current_row][current_col - 1] & 0b0100):
        left = 99
    if current_col < MAX_X - 1 and (wall_info[current_row][current_col] & 0b0100):
        right = 99
    if current_row < MAX_X - 1 and (wall_info[current_row][current_col] & 0b0010):
        down = 99

    # Determine direction
    next_direction = min((up, 0), (left, 3), (right, 1), (down, 2), key=lambda x: x[0])[1]


def rotate_robot():
    '''Rotate the robot in the specified direction'''
    global current_direction
    while current_direction != next_direction:
        if (current_direction - next_direction) % 4 == 1:
            API.turnLeft()
            current_direction = (current_direction - 1) % 4
        else:
            API.turnRight()
            current_direction = (current_direction + 1) % 4
    log_message("Rotating from {} to {}\n".format(current_direction, next_direction))


def advance_robot():
    '''Move the robot forward and update its position'''
    global current_row, current_col
    if is_wall_front:
        return
    if current_direction == 0:  # Up
        current_row -= 1
    elif current_direction == 1:  # Right
        current_col += 1
    elif current_direction == 2:  # Down
        current_row += 1
    elif current_direction == 3:  # Left
        current_col -= 1
    API.moveForward()
    API.setColor(current_col, MAX_X - current_row - 1, 'B')
    log_message("Moved to ({}, {})\n".format(current_row, current_col))


def main():
    log_message("Running...")
    start_time = time.time()
    initialize_flood_fill_path()

    # Setting the starting point and target point
    API.setColor(0, 0, 'R')
    API.setText(0, 0, "Start")
    goal_positions = [((MAX_X//2), (MAX_Y//2)), ((MAX_X//2), (MAX_Y//2)-1), ((MAX_X//2)-1, (MAX_Y//2)), ((MAX_X//2)-1, (MAX_Y//2)-1)]
    for x, y in goal_positions:
        API.setColor(x, y, 'G')
        API.setText(x, y, "Goal")

    # Flood fill and navigate
    while (current_row, current_col) not in goal_positions:
        initialize_flood_fill_path()
        fetch_sensor_data()
        update_wall_info()
        flood_fill(7, 7, 0)
        determine_next_move()
        rotate_robot()
        advance_robot()
    
    end_time = time.time()
    completion_time = end_time - start_time
    log_message("Goal reached at ({}, {})!\n".format(current_row, current_col))
    log_message("Elapsed time: {:.2f} seconds\n".format(completion_time))


if __name__ == "__main__":
    main()
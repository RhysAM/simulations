import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import animation

ALIVE = 1
DEAD = 0
SURVIVES = [2, 3]
BORN = [3]

DIRECTIONS = [(-1, -1), (-1, 1), (-1, 0), (0, 1), (0, -1), (1, 0), (1, -1), (1, 1)]

def make_grid(grid_size, pop):

    size = grid_size[0] * grid_size[1]

    grid = np.zeros(size).astype(int)

    for i in range(pop):

        rand = random.randint(0, size - 1)

        grid[rand] = ALIVE

    grid = grid.reshape(grid_size)

    return grid

def count_live_neighbors(grid, x, y):

    live_count = 0

    for x_direction, y_direction in DIRECTIONS:

        if 0 <= x + x_direction < len(grid) and 0 <= y + y_direction < len(grid[x]):

            live_count += grid[x + x_direction][y + y_direction]

    return live_count


def update_board(old_grid):

    grid = old_grid.copy()

    for i in range(len(grid)):

        for j in range(len(grid[i])):

            live_count = count_live_neighbors(old_grid, i, j)

            if grid[i][j] == ALIVE:

                if live_count not in SURVIVES:

                    grid[i][j] = DEAD
            else:

                if live_count in BORN:

                    grid[i][j] = ALIVE


    return grid

def make_grid_list(number_rounds, grid_size, pop):

    grid = make_grid(grid_size, pop)

    for i in range(number_rounds):

        grid = update_board(grid)

        yield grid

n_frames = 10000
grid = make_grid((100, 100), 1000)
fig, ax = plt.subplots()
matrix = ax.matshow(grid, cmap='binary')


def update(i):

    global grid
    grid = update_board(grid)
    matrix.set_array(grid)

anim = animation.FuncAnimation(fig,update,
    frames=n_frames, interval=50)
plt.show()

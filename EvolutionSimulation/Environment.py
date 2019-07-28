import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import animation
import LivingEntity

FOOD = 2
ALIVE = 1
DEAD = 0


FOOD_SPAWN = 100

class Point:

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def __str__(self):

        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Environment:

    def __init__(self, grid_size, living_pop):

        self.size = grid_size[0] * grid_size[1]

        self.grid = np.zeros(self.size).astype(int)

        self.tick = 0

        for i in range(living_pop):
            rand = random.randint(0, self.size - 1)

            self.grid[rand] = ALIVE

        self.grid = self.grid.reshape(grid_size)

        self.living = list()
        self.food = list()

        self.spawn_food()

        self.get_living()

        self.living_count = list()
        self.speeds = list()
        self.ages = list()

    def display(self):

        fig, ax = plt.subplots()
        ax.imshow(self.grid, cmap='hot')
        plt.show()

    def get_living(self):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == ALIVE:
                    self.living.append(LivingEntity.LivingEntity(i, j, self))

    def get_food(self):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == FOOD:
                    self.food.append(Point(i, j))

    def get_value(self, point):

        return self.grid[point.x][point.y]

    def set_value(self, point, value):

        self.grid[point.x][point.y] = value

    def spawn_food(self):

        for i in range(FOOD_SPAWN):

            x = random.randint(0, len(self.grid) - 1)
            y = random.randint(0, len(self.grid[x]) - 1)

            point = Point(x, y)

            self.set_value(point, FOOD)
            self.food.append(point)

    def get_average_speed(self):

        total_speed = 0

        if len(self.living) == 0:

            return 0

        for entity in self.living:

            total_speed += entity.speed

        return total_speed / len(self.living)

    def get_average_age(self):

        total_age = 0

        if len(self.living) == 0:
            return 0

        for entity in self.living:
            total_age += entity.age

        return total_age / len(self.living)

    def reset_day(self):

        for entity in self.living:

            entity.update_day()

        self.spawn_food()
        self.living_count.append(len(self.living))
        self.speeds.append(self.get_average_speed())
        self.ages.append(self.get_average_age())

    def out_of_energy(self):

        resting = True

        for entity in self.living:

            if entity.energy > 0 and not entity.resting:

                return False

        return True

    def update(self):

        for entity in self.living:

            entity.update()
            self.tick += 1

            if len(self.food) == 0 or self.out_of_energy():
                self.reset_day()

if __name__ == "__main__":

    env = Environment((500, 500), 5)

    showAnimation = False

    if showAnimation:

        fig, ax = plt.subplots()
        matrix = ax.matshow(env.grid, cmap='coolwarm')

        def animate(i):

            env.update()
            matrix.set_array(env.grid)

        anim = animation.FuncAnimation(fig, animate,
                                    frames=10000000000, interval=50)
        plt.show()
    else:

        for i in range(100000):
            env.update()

        f1 = plt.figure()
        f2 = plt.figure()
        f3 = plt.figure()

        ax1 = f1.add_subplot(111)
        ax1.plot(env.living_count)
        ax1.set_ylim(0)
        ax1.set_title("Population each day")
        ax2 = f2.add_subplot(111)
        ax2.plot(env.speeds)
        ax2.set_ylim(0)
        ax2.set_title("Average speed per day")

        ax3 = f3.add_subplot(111)
        ax3.plot(env.ages)
        ax3.set_title("Ages")
        ax3.set_ylim(0)
        plt.show()

        oldest = float("-inf")
        for entity in env.living:
            oldest = max(oldest, entity.age)

        print("The oldest creature is " + str(oldest) + " days old.")

    with open("results.txt", "a") as f:

        for count in env.living_count:
            f.write(str(count))
            f.write(",")
        f.write("\n")
        for speed in env.speeds:
            f.write(str(speed))
            f.write(",")
        f.write("\n")

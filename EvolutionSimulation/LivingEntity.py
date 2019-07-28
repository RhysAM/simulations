import Environment
import random

DEFAULT_ENERGY = 100
DEFAULT_SPEED = 4
ENERGY_CONSUMPTION = .5

class LivingEntity:

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    def __init__(self, x, y, env):

        self.point = Environment.Point(x, y)
        self.closest_food = None
        self.env = env

        self.energy = DEFAULT_ENERGY

        self.speed = DEFAULT_SPEED

        self.consumed = 0
        self.resting = False

        self.age = 0

    def die(self):

        self.env.set_value(self.point, Environment.DEAD)
        self.env.living.remove(self)

    def update(self):

        for i in range(self.speed):
            self.move_to_food()

    def move(self, direction):

        self.energy -= ENERGY_CONSUMPTION * self.speed

        if self.energy <= 0:

            return

        if direction == LivingEntity.DOWN:

            if self.point.x != len(self.env.grid) - 1:

                self.env.set_value(self.point, Environment.DEAD)
                self.point.x += 1
                self.env.set_value(self.point, Environment.ALIVE)

        elif direction == LivingEntity.UP:

            if self.point.x != 0:

                self.env.set_value(self.point, Environment.DEAD)
                self.point.x -= 1
                self.env.set_value(self.point, Environment.ALIVE)

        elif direction == LivingEntity.LEFT:

            if self.point.y != 0:

                self.env.set_value(self.point, Environment.DEAD)
                self.point.y -= 1
                self.env.set_value(self.point, Environment.ALIVE)

        elif direction == LivingEntity.RIGHT:

            if self.point.y != len(self.env.grid[self.point.x]) - 1:

                self.env.set_value(self.point, Environment.DEAD)
                self.point.y += 1
                self.env.set_value(self.point, Environment.ALIVE)

    def find_closest_food(self):

        if (self.closest_food is not None) and (self.env.get_value(self.closest_food) == Environment.FOOD):

            return

        closest_distance = float("inf")

        if len(self.env.food) == 0:

            self.closest_food = None

        for food in self.env.food:

            x_distance = (food.x - self.point.x) ** 2

            y_distance = (food.y - self.point.y) ** 2

            current_distance = x_distance + y_distance

            if closest_distance > current_distance:

                self.closest_food = food
                closest_distance = current_distance

    def move_to_food(self):

        if (self.closest_food is None) or (self.env.get_value(self.closest_food) != Environment.FOOD):

            self.find_closest_food()

        if self.closest_food is None or self.resting:

            return

        if self.closest_food.x == self.point.x and self.closest_food.y == self.point.y:

            self.consume(self.closest_food)
            return

        if self.point.x == self.closest_food.x:

            if self.point.y > self.closest_food.y:

                self.move(LivingEntity.LEFT)

            else:

                self.move(LivingEntity.RIGHT)

        else:

            if self.point.x > self.closest_food.x:

                self.move(LivingEntity.UP)

            else:

                self.move(LivingEntity.DOWN)

    def consume(self, food_point):

        self.env.food.remove(food_point)
        self.closest_food = None

        self.consumed += 1

        if self.consumed == 2:
            self.resting = True

    def reproduce(self):

        if self.point.y != 0:

            child = LivingEntity(self.point.x, self.point.y - 1, self.env)

            self.env.living.append(child)

            child.generate_random_traits(self)

        self.energy -= 50

    def generate_random_traits(self, parent):

        inheritance = random.random()

        if inheritance < .5:

            self.speed = parent.speed

        elif inheritance < .75:

            self.speed = parent.speed + 1

        else:

            if parent.speed != 1:

                self.speed = parent.speed - 1

            else:

                self.speed = parent.speed

    def update_day(self):

        if self.consumed == 0:
            self.die()

        self.energy = DEFAULT_ENERGY

        if self.consumed > 1:
            self.reproduce()

        self.consumed = 0
        self.resting = False
        self.age += 1

    def __repr__(self):

        return str(self.point)
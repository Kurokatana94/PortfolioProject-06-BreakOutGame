from random import randrange
from turtle import Turtle


# Gets a random starting and reset position to differentiate each game session
def _get_random_pos():
    return randrange(-200, 200), randrange(-200, -150)

#Brick class - takes few arguments that are self-explanatory and a speed modifier which will accelerate the ball by that amount until it hits another brick
# (or maybe making it combo dependant?)
class Brick(Turtle):
    def __init__(self, color: str, pos: tuple[float, float], speed_mod=1):
        super().__init__()
        self.shape('square')
        self.shapesize(2, 3)
        self.color(color)
        self.speed(0)
        self.penup()
        self.goto(pos)
        self.speed_mod = speed_mod

#Paddle class (player) ----------------------------------------------------
class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self._INITIAL_POS = (0, -230)
        self.SPEED = 40
        self.LEFT = 180
        self.RIGHT = 0
        self.shape('square')
        self.shapesize(1, 6)
        self.color('white')
        self.speed(0)
        self.penup()
        self.goto(self._INITIAL_POS)

    # Paddle movement and directioning
    def move(self):
        if self.heading() == self.RIGHT:
            target_pos = tuple(self.pos())
            self.goto(target_pos)
        elif self.heading() == self.LEFT:
            target_pos = tuple(self.pos())
            self.goto(target_pos)
        self.forward(self.SPEED)

    def go_right(self):
        if self.pos()[0] < 340:
            self.setheading(self.RIGHT)
            self.move()

    def go_left(self):
        if self.pos()[0] > -340:
            print(self.pos()[0])
            self.setheading(self.LEFT)
            self.move()

#Ball class -----------------------------------------------------------------
class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.shapesize(1, 1)
        self.color('white')
        self.speed(0)
        self.penup()
        self.goto(_get_random_pos())
        self.y_speed = 10
        self.x_speed = 10
        self.move_speed = .04
        self.move()

    # Ball behavior on collision and general movement
    def move(self):
        new_x = self.xcor() + self.x_speed * .66
        new_y = self.ycor() + self.y_speed * .66
        self.setpos(new_x, new_y)

    def y_bounce(self):
        self.x_speed *= -1

    def x_bounce(self):
        self.y_speed *= -1

    def xy_bounce(self):
        self.y_speed *= -1
        self.x_speed *= -1

    # Resets to starting position in a random area range
    def reset_pos(self):
        self.goto(_get_random_pos())
        self.x_speed = 10 if self.x_speed > 0 else -10
        self.y_speed = 10
from turtle import Screen
from tkinter import messagebox, Tk
from elements import Brick, Paddle, Ball
from time import sleep


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Window init
screen = Screen()
screen.bgcolor("black")
screen.title("Break Out")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)
screen.listen()

#paddle init
paddle = Paddle()

#Bricks to break init separated by types
green_bricks = [Brick('green', (n*SCREEN_WIDTH/11, 50), speed_mod=1.01) for n in range(-5, 6)]
yellow_bricks = [Brick('orange', (n*SCREEN_WIDTH/11, 100), speed_mod=1.02) for n in range(-5, 6)]
red_bricks = [Brick('red', (n*SCREEN_WIDTH/11, 150), speed_mod=1.07) for n in range(-5, 6)]

#Ball init
ball = Ball()

screen.onkeypress(key="Right", fun=paddle.go_right)
screen.onkeypress(key="d", fun=paddle.go_right)
screen.onkeypress(key="Left", fun=paddle.go_left)
screen.onkeypress(key="a", fun=paddle.go_left)

is_running = True

def check_brick_hit(brick_list):
    for brick in brick_list:
        if ball.distance(brick) <= 40 and brick.pos()[1]+30 > ball.pos()[1] > brick.pos()[1]-30:
            ball.x_speed *= brick.speed_mod
            ball.y_speed *= brick.speed_mod
            ball.y_bounce()
            brick.reset()
            brick_list.remove(brick)
        elif ball.distance(brick) <= 40 and brick.pos()[1]+50 > ball.pos()[1] > brick.pos()[1]-50:
            ball.x_bounce()
            brick.reset()
            brick_list.remove(brick)

def check_paddle_bounce():
    if ball.distance(paddle) < 70 and ball.pos()[1] <= paddle.pos()[1]+20:
        if ball.pos()[0] < paddle.pos()[0]-20 and ball.x_speed > 0:
            ball.xy_bounce()
        elif ball.pos()[0] > paddle.pos()[0]+20 and ball.x_speed < 0:
            ball.xy_bounce()
        else:
            ball.x_bounce()

def check_wall_bounce():
    if abs(ball.pos()[0]) >= SCREEN_WIDTH/2 - 20:
        ball.y_bounce()
    elif ball.pos()[1] >= SCREEN_HEIGHT/2 - 20:
        ball.x_bounce()

def check_out_of_bonds():
    if ball.pos()[1] <= SCREEN_HEIGHT*-1/2 + 20:
        ball.reset_pos()

# Create a window for the game start
def start_game_popup():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    # Ask the user whether they want to play again or quit
    start = messagebox.askyesno(
        title="Welcome to Break Out",
        message="Are you ready to Play?\n\nPress Yes to start\n\nMove the Paddle with '↔' or 'a' & 'd'"
    )
    root.destroy()

    if not start:
        screen.bye()

# Create a window for the game over
def game_over_popup():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    # Ask the user whether they want to play again or quit
    play_again = messagebox.askyesno(
        title="Game Over",
        message="All bricks destroyed!\n\nWould you like to play again?",
    )
    root.destroy()
    return play_again

# Repositions all elements in their original locations doing a de-facto reset of the game
def reset_game():
    global green_bricks
    global yellow_bricks
    global red_bricks

    paddle.goto(0, -230)
    ball.reset_pos()
    ball.x_speed = 10
    ball.y_speed = 10

    green_bricks = [Brick('green', (n*SCREEN_WIDTH/11,  50)) for n in range(-5, 6)]
    yellow_bricks = [Brick('orange',(n*SCREEN_WIDTH/11, 100), speed_mod=1.02) for n in range(-5, 6)]
    red_bricks    = [Brick('red',   (n*SCREEN_WIDTH/11, 150), speed_mod=1.05) for n in range(-5, 6)]

def game_over():
    if game_over_popup():
        reset_game()     # user chose “Yes”: restart
    else:
        screen.bye()

def check_if_game_over():
    if len(green_bricks) + len(yellow_bricks) + len(red_bricks) == 0:
        game_over()

def game_events():
    check_if_game_over()
    sleep(ball.move_speed)
    screen.update()
    [check_brick_hit(brick_list) for brick_list in (green_bricks, yellow_bricks, red_bricks)]
    check_paddle_bounce()
    check_wall_bounce()
    check_out_of_bonds()
    ball.move()

start_game_popup()

while is_running:
    game_events()
import tkinter
from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 800
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
OBSTACLE_NUM = 3
SNAKE_COLOR = "#00ff00"
FOOD_COLOR = "#fff000"
OBSTACLE_COLOR = "#ff0000"
BACKGROUND_COLOR = "#000000"


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            # the coordinates for each body part at the start of the game will be [0, 0], so that the snake will appear
            # in the top left corner
            self.coordinates.append([0, 0])

        # draw the snake
        # coordinates list is a nested list
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):
        # randomly pick a number from [0,13]
        # * SPACE_SIZE -> convert to
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        # draw the food in the game board
        # x&y are starting coordinate, x + SPACE_SIZE & y + SPACE_SIZE are the ending coordinate
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

class Obstacle:

    def __init__(self):
        self.obstacle_num = OBSTACLE_NUM
        self.coordinates = []
        self.square = []

        for i in range(0, OBSTACLE_NUM):
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            for p in range(0, OBSTACLE_NUM):
                self.coordinates.append([x, y])

        for o, z in self.coordinates:
            canvas.create_rectangle(o, z, o + SPACE_SIZE, z + SPACE_SIZE, fill=OBSTACLE_COLOR, tag="obstacle")



def next_turn(snake, food, obstacle):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    # if the snake and food overlap
    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    # did not eat the food object then delete the last body part
    else:

        # delete the last body part of the snake
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake, obstacle):
        game_over()
    elif check_obstacle(snake, obstacle):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food, obstacle)


def change_direction(new_direction):
    global direction

    # make sure not let the snake ture 180 degrees
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake, obstacle):
    x, y = snake.coordinates[0]

    # check if the snake cross the left or right border
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    elif x == obstacle.coordinates[0] and y == obstacle.coordinates[1]:
        return True

    # check if the snake hit itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True


def check_obstacle(snake, obstacle):
    x, y = snake.coordinates[0]

    for i, j in obstacle.coordinates:
        if x == i and y == j:
            return True
    return False


# prompt game over in the game board
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("time new roman", 70),
                       text="GAME OVER", fill='red', tag="gameover")


window = Tk()
window.title("Greedy Snake")
window.resizable(False, False)
window.iconphoto(False, tkinter.PhotoImage(file="snake.png"))

# initial score
score = 0
# set the initial direction
direction = "right"

# show the score
label = Label(window, text="Score:{}".format(score), font=('time new roman', 45))
label.pack()

# show the game board
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()
obstacle = Obstacle()

next_turn(snake, food, obstacle)

window.mainloop()

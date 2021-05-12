import curses
from random import randrange
import game_config
from game_config import Position
import graphic
import Snake
import time


class Game:
    def __init__(self) -> None:
        self.start_time = time.time()

        self.foods = []
        self.lives = game_config.snake_config["lives"]
        self.scores = 0
        self.highest_score = 0
        self.game_flag = True
        self.graphic = graphic.Graphic()
        self.snake = Snake.Snake()

    def start(self) -> None:
        self.reset()

        while self.game_flag:
            self.graphic.draw_game(self.snake, self.foods, self.lives, self.scores, self.highest_score)

            if not self.update_control():
                continue
            if time.time() - self.start_time < 0.6:
                continue

            self.start_time = time.time()
            self.update_snake()

    def reset(self) -> None:
        self.foods = []
        self.lives = game_config.snake_config["lives"]
        self.scores = 0
        self.highest_score = 0
        self.game_flag = True
        self.snake.reset()
        self.span_food()

    def update_snake(self) -> None:
        self.snake.update_snake_pos()
        index = self.snake.check_eat_food(self.foods)
        if index != -1:
            self.scores += 1
            if len(self.snake.body) >= (self.snake.window_size.x - 2) * (self.snake.window_size.y - 2):  # 蛇身已经填满游戏区域
                self.win()
            else:
                self.span_food()

        if not self.snake.check_alive():
            self.game_over()

    def update_control(self) -> bool:
        key = self.graphic.game_area.getch()

        # 不允许 180度 转弯
        if key == curses.KEY_UP and self.snake.direction != game_config.D_Down:
            self.snake.direction = game_config.D_Up
        elif key == curses.KEY_DOWN and self.snake.direction != game_config.D_Up:
            self.snake.direction = game_config.D_Down
        elif key == curses.KEY_LEFT and self.snake.direction != game_config.D_Right:
            self.snake.direction = game_config.D_Left
        elif key == curses.KEY_RIGHT and self.snake.direction != game_config.D_Left:
            self.snake.direction = game_config.D_Right
        elif key == game_config.keys['Q']:
            self.game_flag = False
            return False
        elif key == game_config.keys['R']:
            self.reset()
            return False

        return True

    def span_food(self) -> None:
        flag = False
        food = Position(0, 0)
        while not flag:
            food.x = randrange(0, self.snake.window_size.x, 1)
            food.y = randrange(0, self.snake.window_size.y, 1)
            flag = self.snake.is_valid_position(food)
        self.foods.append(food)

    def win(self):
        self.game_flag = False
        self.graphic.draw_game(self.snake, self.foods, self.lives, self.scores, self.highest_score)
        text1 = "You Win!"
        text2 = "Your score is %d" % max(self.scores, self.highest_score)
        self.graphic.draw_message_window([text1, text2])
        self.reset()

    def game_over(self):
        if self.lives > 1:
            self.lives -= 1
            self.highest_score = max(self.highest_score, self.scores)
            self.scores = 0
            self.snake.reset()
            self.foods = []
            self.span_food()
            curses.flash()
            return

        self.game_flag = False
        self.lives -= 1
        self.graphic.draw_game(self.snake, self.foods, self.lives, self.scores, self.highest_score)
        text1 = "Game over!"
        text2 = "Your score is %d" % max(self.scores, self.highest_score)
        self.graphic.draw_message_window([text1, text2])
        self.reset()

    def quit(self):
        curses.endwin()

import game_config
from game_config import Position
from Snake import Snake
import curses
import time
import copy


class Graphic:
    def __init__(self) -> None:
        self.target_fps = 50
        self.true_fps = 50
        self.window = curses.initscr()

        # 让游戏窗口居中
        self.window_height = game_config.game_sizes['height']
        self.window_width = game_config.game_sizes['width']

        x = (self.window.getmaxyx()[1] - self.window_width) / 2
        y = (self.window.getmaxyx()[0] - self.window_height) / 2
        if x < 0 or y < 2:
            raise ValueError('Not enough space to display the game.')
        self.game_area_pos = Position(int(x), int(y))
        self.game_area = self.window.subwin(self.window_height, self.window_width,
                                            self.game_area_pos.y, self.game_area_pos.x)
        self.game_area.nodelay(True)
        self.game_area.keypad(True)
        self.last_time = time.time()
        self.delay_time = 0.02
        self.fps_update_interval = 4
        self.frame_count = 0

        curses.curs_set(0)
        curses.start_color()

        curses.init_pair(1, *game_config.game_themes["colors"]["default"])
        curses.init_pair(2, *game_config.game_themes["colors"]["snake"])
        curses.init_pair(3, *game_config.game_themes["colors"]["food"])
        curses.init_pair(4, *game_config.game_themes["colors"]["lives"])

        self.C_default = curses.color_pair(1)
        self.C_snake = curses.color_pair(2)
        self.C_food = curses.color_pair(3)
        self.C_lives = curses.color_pair(4)

    def draw_snake_body(self, snake: Snake) -> None:
        for item in snake.body:
            self.game_area.addch(item.y, item.x,
                                 game_config.game_themes["tiles"]["snake_body"],
                                 self.C_snake)

    def draw_foods(self, foods) -> None:
        for item in foods:
            self.game_area.addch(item.y, item.x,
                                 game_config.game_themes["tiles"]["food"],
                                 self.C_food)

    def draw_border(self) -> None:
        self.game_area.border()

    def draw_help(self):
        helps = ["Help:",
                 "Press: direction key to change direction",
                 "Press 'R' to reset",
                 "Press 'Q' to quit"]
        pos = Position(0, 0)
        for help_text in helps:
            self.window.addstr(pos.y, pos.x, help_text)
            pos.y += 1

    def draw_game(self, snake: Snake, foods, lives, scores, highest_score) -> None:
        self.window.erase()
        self.draw_help()
        self.update_fps()
        self.draw_fps()
        self.draw_lives_and_scores(lives, scores, highest_score)
        self.draw_border()
        self.draw_foods(foods)
        self.draw_snake_body(snake)
        self.window.refresh()
        self.game_area.refresh()
        time.sleep(self.delay_time)

    def draw_fps(self) -> None:
        text = "fps: %.1f" % self.true_fps
        pos = copy.deepcopy(self.game_area_pos)
        pos.y -= 2
        self.draw_text(self.window,
                       pos, text, self.C_default)

    def draw_lives_and_scores(self, lives, scores, highest_score):
        text = "lives: "
        pos = copy.deepcopy(self.game_area_pos)
        pos.y -= 1
        self.draw_text(self.window,
                       pos, text,
                       self.C_default)

        pos.x += len(text)
        text = lives * game_config.game_themes["tiles"]["lives"]
        self.draw_text(self.window,
                       pos, text,
                       self.C_lives)

        pos.x += len(text)
        text = "scores: {} highest_socre: {}".format(scores, highest_score)
        self.draw_text(self.window,
                       pos, text,
                       self.C_default)

    def draw_text(self, win, pos, text, attr=None) -> None:
        win.addstr(pos.y, pos.x, text, attr)

    def draw_message_window(self, texts: list) -> None:  # 接收一个 str 列表
        text1 = "Press any key to continue."
        nrows = 6 + len(texts)  # 留出行与行之间的空隙
        ncols = max(*[len(len_tex) for len_tex in texts], len(text1)) + 20

        x = (self.window.getmaxyx()[1] - ncols) / 2
        y = (self.window.getmaxyx()[0] - nrows) / 2
        pos = Position(int(x), int(y))
        message_win = curses.newwin(nrows, ncols, pos.y, pos.x)
        message_win.nodelay(False)
        # 绘制文字提示
        # 底部文字居中
        pos.y = nrows - 2
        pos.x = self.get_middle(ncols, len(text1))
        message_win.addstr(pos.y, pos.x, text1, self.C_default)

        pos.y = 2
        for text in texts:
            pos.x = self.get_middle(ncols, len(text))
            message_win.addstr(pos.y, pos.x, text, self.C_default)
            pos.y += 1

        message_win.border()
        message_win.refresh()
        message_win.getch()

        message_win.nodelay(True)
        message_win.clear()
        del message_win

    def get_middle(self, win_len, text_len) -> int:
        return int((win_len - text_len) / 2)

    def esp_fps(self) -> bool:  # 返回是否更新了fps
        # 每两帧计算一次
        if self.frame_count < self.fps_update_interval:
            self.frame_count += 1
            return False
        time_span = time.time() - self.last_time
        self.last_time = time.time()
        self.true_fps = 1.0 / (time_span / self.frame_count)
        self.frame_count = 0
        return True

    def update_fps(self) -> None:
        if self.esp_fps():
            err = self.true_fps - self.target_fps
            self.delay_time += 0.00001 * err

    def quite(self):
        pass

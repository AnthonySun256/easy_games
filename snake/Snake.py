import game_config
from game_config import Position
import copy


class Snake(object):
    def __init__(self) -> None:
        self.window_size = Position(game_config.game_sizes["width"], game_config.game_sizes["height"])
        self.direction = game_config.D_Down
        self.body = []
        self.last_body = []
        for i in range(3):
            self.body.append(Position(2, 3 - i))

    def reset(self) -> None:
        self.direction = game_config.D_Down
        self.body = []
        self.last_body = []
        for i in range(3):
            self.body.append(Position(2, 3 - i))

    def get_dis_inc_factor(self) -> Position:
        dis_increment_factor = Position(0, 0)

        # 修改每个方向上的速度
        if self.direction == game_config.D_Up:
            dis_increment_factor.y = -1
        elif self.direction == game_config.D_Down:
            dis_increment_factor.y = 1
        elif self.direction == game_config.D_Left:
            dis_increment_factor.x = -1
        elif self.direction == game_config.D_Right:
            dis_increment_factor.x = 1

        return dis_increment_factor

    def update_snake_pos(self) -> None:
        dis_increment_factor = self.get_dis_inc_factor()
        self.last_body = copy.deepcopy(self.body)

        for index, item in enumerate(self.body):
            if index < 1:
                item.x += dis_increment_factor.x
                item.y += dis_increment_factor.y
            else:  # 剩下的部分要跟着前一部分走
                item.x = self.last_body[index - 1].x
                item.y = self.last_body[index - 1].y

    def check_alive(self) -> bool:  # 检查是否死亡
        flag1 = self.check_eat_self()
        flag2 = self.check_hit_wall()
        return not (flag1 or flag2)

    def eat_food(self, food) -> None:
        self.body.append(self.last_body[-1])  # 长大一个元素

    def check_eat_food(self, foods: list) -> int:  # 返回吃到了哪个苹果
        for index, food in enumerate(foods):
            if food == self.body[0]:
                self.eat_food(food)
                foods.pop(index)
                return index
        return -1

    def check_eat_self(self) -> bool:
        return self.body[0] in self.body[1:]  # 判断蛇头是不是和身体重合

    def check_hit_wall(self) -> bool:
        is_between_top_bottom = self.window_size.y - 1 > self.body[0].y > 0
        is_between_left_right = self.window_size.x - 1 > self.body[0].x > 0
        return not (is_between_top_bottom and is_between_left_right)

    def is_valid_position(self, pos: Position) -> bool:
        # 我想过用这个函数替换检查吃自己和撞墙，但我认为也许单独写一个也许会更好一点
        flag1 = not (pos in self.body)
        flag2 = self.window_size.y - 1 > pos.y > 0 and \
                self.window_size.x - 1 > pos.x > 0
        return flag1 and flag2

    def get_relative_direction(self, pos1: Position, pos2: Position) -> int:
        # 返回 pos1 在 pos2 的上（下左右）边
        # 默认两个点是在一行（列）上的
        x_inc = pos1.x - pos2.x
        y_inc = pos1.y - pos2.y
        if 0 != x_inc and 0 != y_inc:
            raise ValueError

        if x_inc > 0:
            return game_config.D_Right
        elif x_inc < 0:
            return game_config.D_Left
        elif y_inc > 0:
            return game_config.D_Down
        elif y_inc < 0:
            return game_config.D_Up

        raise ValueError

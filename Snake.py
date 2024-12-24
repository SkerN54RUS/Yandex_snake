from random import randint

import pygame as pg

from sys import exit

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Центр экрана:
DEFAULT_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 25, 25)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Начальная длинна змейки
LENGTH = 1

# Скорость движения змейки:
SPEED = 10

# Для проверки столконовения змейки с собой:
CHECKED_LENGTH = 4


# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Заголовок окна игрового поля:
pg.display.set_caption("Змейка")

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс создания игрового поля."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR, position=DEFAULT_POSITION):

        self.body_color = body_color
        self.position = position

    def draw():
        """Отрисовка поля."""

    def draw_cell(self, position, body_color, border_color=BORDER_COLOR):
        """Отрисовывает одну клетку на игровом поле."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, body_color=APPLE_COLOR, snake_positions=None):
        super().__init__(body_color)
        self.position = self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions=None):

        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x, y)
            if snake_positions is None or position not in snake_positions:
                break
        return position

    def draw(self):
        """Параметры изображения яблока."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс Змеи"""

    def __init__(self, length=LENGTH, direction=RIGHT, next_direction=RIGHT, last=None):

        super().__init__(body_color=SNAKE_COLOR)
        self.reset(length, direction, next_direction, last)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения."""
        # Вычисляем новую позицию головы
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        head_x = (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        head_y = (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        # Добавляю новую позицию головы
        self.positions.insert(0, (head_x, head_y))
        # Обрабатываю хвост змеики
        if len(self.positions) - 1 >= self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Параметры изображения змеи."""
        # Если голова пройдет перпендикулярно к хвосту, и разминется
        # с ним буквально на фрейм, то затрется один блок, и будет черным.
        # Поэтому оставляю перерисовку всей змейки, с головой.
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        """Отрисовка головы змеи."""
        self.draw_cell(self.positions[0], self.body_color)

        """Затирание последнего сегмента."""
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Начало змеики"""
        return self.positions[0]

    def reset(self, length=LENGTH, direction=RIGHT, next_direction=RIGHT, last=None):
        """Сброс до начального отображения."""
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.last = last
        self.positions = [self.position]


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            # raise SystemExit
            exit(0)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запуск выполнения кода."""

    pg.init()
    snake = Snake()
    apple = Apple(snake_positions=snake.positions)

    """Запуск цикла"""
    while True:

        pg.display.update()

        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # apple.draw()
        # snake.draw()

        # if snake.next_direction is not None:
        #     snake.update_direction()
        #     snake.move()
        #     screen.fill(BOARD_BACKGROUND_COLOR)
        #     apple.draw()
        #     snake.draw()

        # Тут опишите основную логику игры.

        # Если змейка сьедает яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake_positions=snake.positions)

        # Змея врезается в себя.

        # for position in snake.position[1:]:
        #     if snake.get_head_position() == position:
        #         snake.reset()
        if snake.length > CHECKED_LENGTH and snake.get_head_position() in snake.positions[CHECKED_LENGTH:]:
            snake.reset()
            apple.randomize_position(snake_positions=snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()


if __name__ == "__main__":
    main()

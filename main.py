from queue import Queue
from list_sprites import *
from constants import *
import pygame as pg
import random

HEIGHT = 10
WIDTH = 20


class Map:
    def __init__(self):
        self.road_matrix = []
        for i in range(WIDTH):
            self.road_matrix.append([0] * HEIGHT)
        self.generate_road_matrix()

        self.grid_matrix = []
        for i in range(WIDTH):
            self.grid_matrix.append([0] * HEIGHT)
        self.generate_start_grid()
        self.change_road()
        self.generate_city()


    def generate_road_matrix(self):
        for i in range(0, 5):
            self.road_matrix[0][i] = 1
        self.road_matrix[1][4] = 1
        q = Queue()
        q.put((1, 4))
        while 1 not in self.road_matrix[18]:
            if q.empty():
                list_ones = []
                for i in range(18, -1, -1):
                    if 1 in self.road_matrix[i]:
                        for j in range(10):
                            if self.road_matrix[i][j] == 1:
                                list_ones.append((i, j))
                            if j == 9:
                                q.put(random.choice(list_ones))
                                list_ones = []
                                break
                        if not q.empty():
                            break
            while not q.empty():
                x, y = q.get()
                neighbours = self.find_neighbours(x, y)
                right = True
                up = True
                down = True
                if (x - 1, y - 1) in neighbours or (x - 1, y - 1) in neighbours:
                    up = False
                if (x + 1, y - 1) in neighbours and (x, y - 1) in neighbours or (x + 1, y + 1) in neighbours and (
                x, y + 1) in neighbours:
                    right = False
                if (x - 1, y + 1) in neighbours or (x + 1, y - 1) in neighbours:
                    down = False
                if right:
                    if random.randint(0, 1):
                        if 0 <= x + 1 <= 18 and 0 <= y <= 9:
                            q.put((x + 1, y))
                            self.road_matrix[x + 1][y] = 1
                if up:
                    if random.randint(0, 1):
                        if 0 <= x <= 18 and 0 <= y - 1 <= 9:
                            q.put((x, y - 1))
                            self.road_matrix[x][y - 1] = 1
                if down:
                    if random.randint(0, 1):
                        if 0 <= x <= 19 and 0 <= y + 1 <= 9:
                            q.put((x, y + 1))
                            self.road_matrix[x][y + 1] = 1
        ind = -1
        for i in range(10):
            if self.road_matrix[18][i]:
                ind = i
        for i in range(ind, 10):
            self.road_matrix[19][i] = 1


    def find_neighbours(self, x, y):
        neighbours = set()
        for i in range (-1, 2):
            for j in range (-1, 2):
                if 0 <= i + x <= 18 and 0 <= y + j <= 9 and self.road_matrix[x + i][y + j] == 1:
                    if not (i == 0 and j == 0):
                        neighbours.add((x + i, y + j))
        return list(neighbours)


    def print_grid_matrix(self):
        for i in range(HEIGHT):
            for j in range(WIDTH):
                print(self.grid_matrix[j][i], end=" ")
            print()


    def print_road_matrix(self):
        for i in range(HEIGHT):
            for j in range(WIDTH):
                print(self.road_matrix[j][i], end=" ")
            print()


    def generate_city(self):
        for elem in max_count_sprite.keys():
            if elem not in big_sprite:
                for x in range(max_count_sprite[elem]):
                    i = random.randint(2, 18)
                    j = random.randint(0, 9)
                    while not len(self.find_neighbours(i, j)) or self.road_matrix[i][j] != 0:
                        i = random.randint(1, 18)
                        j = random.randint(0, 9)
                    self.road_matrix[i][j] = code_sprite[elem]
                    self.grid_matrix[i][j] = code_sprite[elem]
            else:
                for x in range(max_count_sprite[elem]):
                    i = random.randint(2, 17)
                    j = random.randint(0, 9)
                    while not len(self.find_neighbours(i, j)) or self.road_matrix[i][j] != 0 or not len(
                            self.find_neighbours(i - 1, j)) or self.road_matrix[i - 1][j] != 0:
                        i = random.randint(2, 17)
                        j = random.randint(0, 9)
                    self.road_matrix[i - 1][j] = code_sprite[elem]
                    self.grid_matrix[i - 1][j] = code_sprite[elem]
                    self.road_matrix[i][j] = code_sprite[elem]
                    self.grid_matrix[i][j] = code_sprite[elem]
        for i in range(2, 18):
            for j in range(10):
                if len(self.find_neighbours(i, j)) and not self.road_matrix[i][j]:
                    # расставляются маленькие дома
                    self.grid_matrix[i][j] = random.choice([28, 29, 30, 31, 32, 33])


    def change_road(self):
        for i in range(20):
            for j in range(10):
                if i == 0 and self.road_matrix[i][j]:
                    if not self.road_matrix[i + 1][j]:
                        self.grid_matrix[i][j] = 7
                        # sprite "road_vertical.png"
                    else:
                        self.grid_matrix[i][j] = 15
                        # sprite "turn_right_up.png"
                elif 0 < i <= 18:
                    if 0 < j < 9 and self.road_matrix[i][j] == 1:
                        if self.road_matrix[i][j - 1] == 1 and self.road_matrix[i - 1][j] == 1 and self.road_matrix[i + 1][j] == 1 and \
                                self.road_matrix[i][j + 1] == 1:
                            # sprite "cross_road.png"
                            self.grid_matrix[i][j] = 8
                        elif self.road_matrix[i][j - 1] == 1 and self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][
                            j] == 0 and self.road_matrix[i - 1][j] == 0:
                            # sprite "road_vertical.png"
                            self.grid_matrix[i][j] = 7
                        elif self.road_matrix[i][j - 1] == 0 and self.road_matrix[i][j + 1] == 0 and self.road_matrix[i + 1][
                            j] == 1 and self.road_matrix[i - 1][j] == 1:
                            # sprite "road_horisontal.png"
                            self.grid_matrix[i][j] = 6
                        elif self.road_matrix[i][j - 1] == 0 and self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][
                            j] == 0 and self.road_matrix[i - 1][j] == 1:
                            # sprite "turn_left_down.png"
                            self.grid_matrix[i][j] = 14
                        elif self.road_matrix[i][j - 1] == 1 and self.road_matrix[i][j + 1] == 0 and self.road_matrix[i + 1][
                            j] == 0 and self.road_matrix[i - 1][j] == 1:
                            # sprite "turn_left_up.png"
                            self.grid_matrix[i][j] = 13
                        elif self.road_matrix[i][j - 1] == 1 and self.road_matrix[i][j + 1] == 0 and self.road_matrix[i + 1][
                            j] == 1 and self.road_matrix[i - 1][j] == 0:
                            # sprite "turn_right_up.png"
                            self.grid_matrix[i][j] = 15
                        elif self.road_matrix[i][j - 1] == 0 and self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][
                            j] == 1 and self.road_matrix[i - 1][j] == 0:
                            # sprite "turn_right_down.png"
                            self.grid_matrix[i][j] = 16
                        elif self.road_matrix[i][j - 1] == 0 and self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][
                            j] == 1 and self.road_matrix[i - 1][j] == 1:
                            # sprite "cross_road_3_down.png"
                            self.grid_matrix[i][j] = 12
                        elif self.road_matrix[i][j - 1] == 1 and self.road_matrix[i][j + 1] == 0 and self.road_matrix[i + 1][
                            j] == 1 and self.road_matrix[i - 1][j] == 1:
                            # sprite "cross_road_3_up.png"
                            self.grid_matrix[i][j] = 11
                        elif self.road_matrix[i][j - 1] == 1 and self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][
                            j] == 0 and self.road_matrix[i - 1][j] == 1:
                            # sprite "cross_road_3_left.png"
                            self.grid_matrix[i][j] = 10
                        elif self.road_matrix[i][j - 1] == 1 and self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][
                            j] == 1 and self.road_matrix[i - 1][j] == 0:
                            # sprite "cross_road_3_right.png"
                            self.grid_matrix[i][j] = 9
                        elif self.road_matrix[i][j - 1] == 1 and self.road_matrix[i][j + 1] == 0 and self.road_matrix[i + 1][
                            j] == 0 and self.road_matrix[i - 1][j] == 0:
                            # sprite "dead_end_up.png"
                            self.grid_matrix[i][j] = 19
                        elif self.road_matrix[i][j - 1] == 0 and self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][
                            j] == 0 and self.road_matrix[i - 1][j] == 0:
                            # sprite "dead_end_down.png"
                            self.grid_matrix[i][j] = 20
                        elif self.road_matrix[i][j - 1] == 0 and self.road_matrix[i][j + 1] == 0 and self.road_matrix[i + 1][
                            j] == 0 and self.road_matrix[i - 1][j] == 1:
                            # sprite "dead_end_left.png"
                            self.grid_matrix[i][j] = 17
                        elif self.road_matrix[i][j - 1] == 0 and self.road_matrix[i][j + 1] == 0 and self.road_matrix[i + 1][
                            j] == 1 and self.road_matrix[i - 1][j] == 0:
                            # sprite "dead_end_right.png"
                            self.grid_matrix[i][j] = 18
                    elif j == 0 and self.road_matrix[i][j] == 1:
                        if self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][j] == 1 and self.road_matrix[i - 1][j] == 1:
                            # sprite "cross_road_3_down.png"
                            self.grid_matrix[i][j] = 12
                        elif self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][j] == 0 and self.road_matrix[i - 1][j] == 0:
                            # sprite "dead_end_down.png"
                            self.grid_matrix[i][j] = 20
                        elif self.road_matrix[i][j + 1] == 0 and self.road_matrix[i + 1][j] == 0 and self.road_matrix[i - 1][j] == 1:
                            # sprite "dead_end_left.png"
                            self.grid_matrix[i][j] = 17
                        elif self.road_matrix[i][j + 1] == 0 and self.road_matrix[i + 1][j] == 1 and self.road_matrix[i - 1][j] == 0:
                            # sprite "dead_end_right.png"
                            self.grid_matrix[i][j] = 18
                        elif self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][j] == 0 and self.road_matrix[i - 1][j] == 1:
                            # sprite "turn_left_down.png"
                            self.grid_matrix[i][j] = 14
                        elif self.road_matrix[i][j + 1] == 1 and self.road_matrix[i + 1][j] == 1 and self.road_matrix[i - 1][j] == 0:
                            # sprite "turn_right_down.png"
                            self.grid_matrix[i][j] = 16
                        elif self.road_matrix[i][j + 1] == 0 and self.road_matrix[i + 1][j] == 1 and self.road_matrix[i - 1][j] == 1:
                            # sprite "road_horisontal.png"
                            self.grid_matrix[i][j] = 6
                    elif j == 9 and self.road_matrix[i][j] == 1:
                        if self.road_matrix[i][j - 1] == 1 and self.road_matrix[i + 1][j] == 1 and self.road_matrix[i - 1][j] == 1:
                            # sprite "cross_road_3_up.png"
                            self.grid_matrix[i][j] = 11
                        elif self.road_matrix[i][j - 1] == 1 and self.road_matrix[i + 1][j] == 0 and self.road_matrix[i - 1][j] == 0:
                            # sprite "dead_end_up.png"
                            self.grid_matrix[i][j] = 19
                        elif self.road_matrix[i][j - 1] == 0 and self.road_matrix[i + 1][j] == 0 and self.road_matrix[i - 1][j] == 1:
                            # sprite "dead_end_left.png"
                            self.grid_matrix[i][j] = 17
                        elif self.road_matrix[i][j - 1] == 0 and self.road_matrix[i + 1][j] == 1 and self.road_matrix[i - 1][j] == 0:
                            # sprite "dead_end_right.png"
                            self.grid_matrix[i][j] = 18
                        elif self.road_matrix[i][j - 1] == 1 and self.road_matrix[i + 1][j] == 0 and self.road_matrix[i - 1][j] == 1:
                            # sprite "turn_left_up.png"
                            self.grid_matrix[i][j] = 13
                        elif self.road_matrix[i][j - 1] == 1 and self.road_matrix[i + 1][j] == 1 and self.road_matrix[i - 1][j] == 0:
                            # sprite "turn_right_up.png"
                            self.grid_matrix[i][j] = 15
                        elif self.road_matrix[i][j - 1] == 0 and self.road_matrix[i + 1][j] == 1 and self.road_matrix[i - 1][j] == 1:
                            # sprite "road_horisontal.png"
                            self.grid_matrix[i][j] = 6
                elif i == 19 and self.road_matrix[i][j]:
                    if not self.road_matrix[i - 1][j]:
                        # sprite "road_vertical.png"
                        self.grid_matrix[i][j] = 7
                    else:
                        # sprite "turn_left_down.png"
                        self.grid_matrix[i][j] = 14


    def generate_start_grid(self):
        for i in range (20):
            for j in range (10):
                number_sprite = random.randint(1, 5)
                self.grid_matrix[i][j] = number_sprite



def main():
    map = Map()
    def draw_sprite(i, j, name):
        sprite = pg.image.load(name)
        sprite_rect = sprite.get_rect(
            bottomright=(i * block_size + 2 * block_size, j * block_size + 2 * block_size))
        screen.blit(sprite, sprite_rect)
    pg.init()
    screen = pg.display.set_mode(size)
    pg.display.set_caption("PixelCity")
    icon = pg.image.load('../PixelCityGame/sprites/sea.png')
    pg.display.set_icon(icon)
    screen.fill(WHITE)

    # изначальное заполнение поля
    for i in range(20):
        for j in range(10):
            name_sprite = "sprites/" + random.choice(start_sprite_list)
            if map.grid_matrix[i][j] in sprites.keys():
                if not(sprites[map.grid_matrix[i][j]] in big_sprite and map.grid_matrix[i + 1][j] in sprites.keys() and sprites[map.grid_matrix[i + 1][j]] in big_sprite):
                    name_sprite = "sprites/" + sprites[map.grid_matrix[i][j]]
            draw_sprite(i, j, name_sprite)

    pg.display.update()
    game_over = False

    while not game_over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
            pg.display.update()


if __name__ == '__main__':
    main()

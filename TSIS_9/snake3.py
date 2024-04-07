import pygame, sys, random
from pygame.math import Vector2
from pygame import Rect
import sys
import numpy as np
import os 

fps = 60
cell_size = 20
row_number = 30
col_number = 40
screen_size = (cell_size * col_number, cell_size * row_number)
speed = 150
level = 1

class Constants:
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    fruits = {1: "apple", 2: "banana", 3: "strawberry"}

class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.randomize()

    # drawing fruit
    def draw(self, surf):
        surf.blit(self.image, self.rect)

    # randomly placing fruit
    def randomize(self):
        self.weight = 1
        self.pos = Vector2(random.randint(1, col_number - 3), random.randint(1, row_number - 3))
        self.image = pygame.transform.scale(pygame.image.load(os.path.abspath(f"TSIS_9/resources_snake/{Constants.fruits[self.weight]}.png")).convert_alpha(),(cell_size, cell_size))
        # create rectangle
        self.rect = Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)


# Sprite class inherited from pygame Sprite for Snake 
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos_list = [Vector2(8, 10), Vector2(7, 10), Vector2(6, 10)]
        self.direction = Vector2(1, 0)

        self.image = pygame.transform.scale(pygame.image.load("TSIS_8/resources/block.png"), (cell_size, cell_size))

        self.sound = pygame.mixer.Sound('TSIS_8/resources/ding.mp3')
        self.speed = 200

    # drawing snake 
    def draw(self, surf):
        for i, pos in enumerate(self.pos_list):
            rect = Rect(int(pos.x * cell_size), int(pos.y * cell_size), cell_size, cell_size)
            surf.blit(self.image, rect)
           

    # method for moving snake
    def move(self):
        pos_list_copy = self.pos_list[:-1]
        pos_list_copy.insert(0, pos_list_copy[0] + self.direction)
        self.pos_list = pos_list_copy

    # snake eating fruit and increasing its size by 1
    def eat(self):
        pos_list_copy = self.pos_list[:]
        last_index = len(pos_list_copy) - 1
        pos_list_copy.insert(last_index, pos_list_copy[last_index] + self.direction)
        self.pos_list = pos_list_copy

        if (self.speed > 100):
            self.speed = self.speed - 10 * level

        pygame.time.set_timer(screen_update, self.speed)


    # playing eating sound
    def play_sound(self):
        self.sound.play()

    # reset method in the case of game over
    def reset(self):
        self.pos_list = [Vector2(8, 10), Vector2(7, 10), Vector2(6, 10)]
        self.speed = 150
        pygame.time.set_timer(screen_update, self.speed)


# Class with general logic of the game
class GameLogic:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.map = np.ones((col_number, row_number))
        self.map[1:-1, 1:-1] = np.random.choice([0, 1], size=(col_number - 2, row_number - 2), p=[(100 - 5 * level) / 100, level * 5 / 100])
        self.walls_list = []

    # updating the state of the game
    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail_states()

    # drawing game elements
    def draw_elements(self, surf, font, score_text):
        self.draw_background(surf)
        self.draw_walls(surf)
        self.snake.draw(surf)
        self.fruit.draw(surf)
        self.draw_score(surf, score_text, font)

    # checking for collision of snake with fruit
    def check_collision(self):
        if self.fruit.pos == self.snake.pos_list[0]:
            self.fruit.randomize()
            self.snake.eat()
            self.snake.play_sound()

        for pos in self.snake.pos_list:
            if pos == self.fruit.pos:
                self.fruit.randomize()

        for wall in self.walls_list:
            if wall == self.fruit.pos:
                self.fruit.randomize()

    # method running game over case
    def game_over(self):
        self.snake.reset()

    # method for checking all game over states
    def check_fail_states(self):
        # checking if snake collides with walls
        if not 0 <= self.snake.pos_list[0].x < col_number or not 0 <= self.snake.pos_list[0].y < row_number:
            self.game_over()

        # checking if snake head collides with itself
        for snake_part in self.snake.pos_list[1:]:
            if snake_part == self.snake.pos_list[0]:
                self.game_over()
        # if snake hits walls
        for wall in self.walls_list:
            if wall == self.snake.pos_list[0]:
                self.game_over()

    # method for drawing score on the screen
    def draw_score(self, surf, score_text, font):
        score_text = f"""{len(self.snake.pos_list) - 3} / {level} lvl"""
        score_surf = font.render(score_text, True, (255, 220, 0))
        score_surf_pos = (int(cell_size * col_number - 750), int(cell_size * row_number - 580))
        score_rect = score_surf.get_rect(center=score_surf_pos)
        surf.blit(score_surf, score_rect)
        apple = self.fruit.image
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        surf.blit(apple, apple_rect)

    # method for drawing dirt on the ground
    def draw_background(self, surf):
        bg = pygame.image.load("TSIS_8/resources/background.png")
        surf.blit(bg, (0,0))

    # method for drawing walls
    def draw_walls(self, surf):
        wall_img = pygame.image.load('TSIS_8/resources/wall.png')
        wall_img = pygame.transform.scale(wall_img, (cell_size, cell_size))
        wall_rect = wall_img.get_rect()
        for i, y in enumerate(self.map):
            for j, x in enumerate(y):
                if x == 1:
                    self.walls_list.insert(0, Vector2(i, j))
                    wall_rect.topleft = (i * cell_size, j * cell_size)
                    surf.blit(wall_img, wall_rect)


# main method of the game
def main(level=None):
    pygame.init()
    
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    snake_game = GameLogic()
    game_font = pygame.font.SysFont('arial', 20)
 
    global screen_update
    screen_update = pygame.USEREVENT
    pygame.time.set_timer(screen_update, speed)
    while True:
        # running for every user input
        for event in pygame.event.get():
            # quit event type
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # updating the game on each user event
            if event.type == screen_update:
                snake_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                match event.key:
                    case pygame.K_UP:
                        if snake_game.snake.direction != Vector2(0, 1):
                            snake_game.snake.direction = Vector2(0, -1)
                    case pygame.K_DOWN:
                        if snake_game.snake.direction != Vector2(0, -1):
                            snake_game.snake.direction = Vector2(0, 1)
                    case pygame.K_RIGHT:
                        if snake_game.snake.direction != Vector2(-1, 0):
                            snake_game.snake.direction = Vector2(1, 0)
                    case pygame.K_LEFT:
                        if snake_game.snake.direction != Vector2(1, 0):
                            snake_game.snake.direction = Vector2(-1, 0)
        # calculating the score
        score = str(len(snake_game.snake.pos_list) - 3)
        # increasing level and resetting the game
        if score == 5:
            level += 1
            score = 0
            snake_game = GameLogic()
            snake_game.game_over()
        screen.fill((173, 121, 75))
        snake_game.draw_elements(screen, game_font, score)
        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
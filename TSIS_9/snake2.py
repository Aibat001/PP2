import pygame
from pygame.locals import *
from pygame.math import Vector2
import time
import random
import numpy as np

SIZE = 20
SCORE = 0
BACKGROUND_COLOR = (110, 110, 5)
level = 1
speed = 150

class Fruits:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("TSIS_8/resources/apple.png").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("TSIS_8/resources/block.png").convert()
        self.direction = 'down'
        self.speed = 200
        self.length = 1 
        self.x = [20]
        self.y = [20]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")

        pygame.mixer.init()
        self.play_background_music()
        self.walls_list = []
        self.map = np.ones((40, 30))
        self.map[1:-1, 1:-1] = np.random.choice([0, 1], size = (40 - 2, 30 - 2), p = [(100 - 5 * level) / 100, level * 5 / 100])
        self.surface = pygame.display.set_mode((800, 600))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.fruits = Fruits(self.surface)
        self.fruits.draw()

    def play_background_music(self):
        pygame.mixer.music.load('TSIS_8/resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("TSIS_8/resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("TSIS_8/resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.fruits = Fruits(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    def draw_wall(self, surface):
        wall = pygame.image.load("TSIS_8/resources/wall.png")
        wall = pygame.transform.scale(wall, (SIZE, SIZE))
        wall_rect = wall.get_rect()
        for i, y0 in enumerate(self.map):
            for j, x0 in enumerate(y0):
                if x0 == 1:
                    self.walls_list.insert(0, Vector2(i, j))
                    wall_rect.topleft = (i * SIZE, j * SIZE)
                    surface.blit(wall, wall_rect)
    

    def render_background(self):
        bg = pygame.image.load("TSIS_8/resources/background.png")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.display_score()
        self.fruits.draw()
        self.draw_wall()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.fruits.x, self.fruits.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.fruits.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"
            
            

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length - 1}",True,(200,200,200))
        self.surface.blit(score,(690,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 260))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (130, 300))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.15)

if __name__ == '__main__':
    game = Game()
    game.run()
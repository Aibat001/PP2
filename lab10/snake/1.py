import pygame
from random import randint, randrange
import psycopg2
from config import *

config = psycopg2.connect(**params)
current = config.cursor()
username = input('enter your name: ')
current.execute("SELECT id, level FROM snake_user WHERE username = %s", (username,))
result = current.fetchone()
#result = None

if result is not None:
    user_id, level = result
    print("Welcome back, {}! Your current level is {}.".format(username, level))
else:
    # create a new user
    current.execute("INSERT INTO snake_user (username) VALUES (%s) RETURNING id", (username,))
    user_id = current.fetchone()[0]
    level = 1
    print("Welcome, {}! You are starting at level {}.".format(username, level))

pygame.init()

w, h = 800, 800
fps, level, step = 5, 0, 40
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Snake Game')
is_running, lose = True, False
clock = pygame.time.Clock()
score1 = pygame.font.SysFont("Verdana", 20)
surf = pygame.Surface((390, 390), pygame.SRCALPHA)

gameover = pygame.image.load("gameover.jpg")
gameover = pygame.transform.scale(gameover, (390, 390))

flag = False

class Food:
    def __init__(self,im):
        self.x = randrange(0, w, step)
        self.y = randrange(0, h, step)
        self.r = 0
        self.image = im

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def draw2(self):
        self.x = randrange(0, w, step)
        self.y = randrange(0, h, step)
        self.r = randint(1,2)
        self.image = pygame.image.load(f'food{self.r}.png')


class Snake:
    def __init__(self):
        self.speed = step
        self.body = [[360, 360]]  #изначальные координаты головы
        self.dx = 0
        self.dy = 0
        self.score = 0
        self.color = 'green'

    def move(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and self.dx == 0: # чтобы при нажатии налево, змейка не двигалась вправо
                    self.dx = -self.speed
                    self.dy = 0
                if event.key == pygame.K_d and self.dx == 0:
                    self.dx = self.speed
                    self.dy = 0
                if event.key == pygame.K_w and self.dy == 0:
                    self.dx = 0
                    self.dy = -self.speed
                if event.key == pygame.K_s and self.dy == 0:
                    self.dx = 0
                    self.dy = self.speed

        # передвигаем части тела змейки по х и у на предыдущие координаты
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0] = self.body[i - 1][0]
            self.body[i][1] = self.body[i - 1][1]

        # передвигаем голову змейки по х и у на следующие координаты
        self.body[0][0] += self.dx
        self.body[0][1] += self.dy

    def draw(self):
        for part in self.body:
            pygame.draw.rect(screen, self.color, (part[0], part[1], step, step))

    # проверяем когда змейка съедает еду
    def collide_food(self, Food):
        if self.body[0][0] == f.x and self.body[0][1] == f.y: # если координаты головы змейки совпадают с координатами еды
            self.score += 1
            global flag
            flag = True
            self.body.append([1000, 1000])

    # заканчиваем игру, если голова змейки столкнеться со своим телом
    def self_collide(self):
        global is_running
        if self.body[0] in self.body[1:]: # если голова змейки и входит в массив координат тела змейки
            lose = True # запускаем цикл 'game_over'


    # проверяем чтобы еда не оказалась на теле змейки
    def check_food(self, Food):
        if [f.x, f.y] in self.body: # если координаты еды входят в массив координат тела змейки
            f.draw2() # заново рисуем еду


class Wall:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.pic = pygame.image.load("1.jpg")


    def draw(self):
        screen.blit(self.pic, (self.x, self.y))
def disappear(t):
    pygame.time.set_timer(pygame.USEREVENT, t)

# создаем объекты змейки и еды
s = Snake()
f = Food(pygame.image.load(f'food{randint(1,2)}.png'))
disappear(5000)

# запускаем основной цикл
while is_running:
    clock.tick(fps)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    is_running = False
        if event.type == pygame.USEREVENT and flag == False: # еда появляется каждые пять секунд
            f.draw2() # через 5 секунд перерисовывется


    screen.fill((5, 25, 5))

    # прорисовываем стенки с помощью заранее написанных паттернов
    my_walls = open(f'wall{level}.txt', 'r').readlines() # читает каждую линию как отдельный лист
    walls = []
    for i, line in enumerate(my_walls): # проходимся по индексу и строке
        for j, each in enumerate(line): # проходимся по каждому элементу в строке
            if each == "+":
                walls.append(Wall(j * step, i * step)) # добавляем каждый блок стенки в лист

    # вызываем методы классов
    f.draw()
    s.draw()
    s.move(events) # нажать любую клавишу (a, s, d, w) чтобы начать игру
    s.collide_food(f)
    s.self_collide()
    s.check_food(f)

    # высвечиваем текущие баллы и уровень на экран
    counter = score1.render(f'Score: {s.score}', True, 'white')
    screen.blit(counter, (50, 50))
    l = score1.render(f'Level: {level}', True, 'white')
    screen.blit(l, (50, 80))

    # условие для перехода на следующий уровень
    if s.score % 5 == 0:
        level += 1
        level %= 4
        fps += 2
        s.score += 3 # новый счетчик для следующего уровня

    # высвечиваем стенки на экран
    for wall in walls:
        wall.draw()
        if f.x == wall.x and f.y == wall.y: # перерисовываем еду, если она оказалась на стенках
            f.draw2()

        if s.body[0][0] == wall.x and s.body[0][1] == wall.y: # останавливаем игру, если голова змейки столкнеться со стенкой
            lose = True


    # запускаем цикл 'game_over'
    while lose:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                lose = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    '''
                    if s.score == 1:
                        score = 100
                    elif s.score == 2:
                        score = 200
                    elif s.score == 3:
                        score = 300
                    else: score = 0
                    '''
                    current.execute("INSERT INTO score (user_id, score, level) VALUES (%s, %s, %s)",
                                    (user_id, s.score, level))
                    config.commit()
                    print("Score saved at level {}!".format(level))


                    # pause the game
                    paused = True
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    paused = False

        surf.blit(gameover, (0, 0))
        screen.blit(surf, (200, 200))
        cntr = score1.render(f'Your score is {s.score}', True, 'white')
        screen.blit(cntr, (320, 405))
        l = score1.render(f'Your level is {level}', True, 'white')
        screen.blit(l, (322, 435))
        pygame.display.flip()
    pygame.display.flip()
pygame.quit()
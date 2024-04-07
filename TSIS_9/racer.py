import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 390
SCREEN_HEIGHT = 600
SPEED = 5
SCORE1 = 0
SCORE2 = 0
SONG_END = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(SONG_END)
pygame.mixer.music.load('TSIS_8/resources/fone.wav')
pygame.mixer.music.play()

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
lose = font_small.render("You lose!", True, BLACK)


background = pygame.image.load("TSIS_8/resources/AnimatedStreet.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((390, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("TSIS_8/resources/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

      def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("TSIS_8/resources/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
        if self.rect.left > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.right < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)

class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("TSIS_8/resources/coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(10, SCREEN_WIDTH - 10), 25)

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 25)

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coins()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
bonus = pygame.sprite.Group()
bonus.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1


#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    DISPLAYSURF.blit(background, (0, 0))
    scores1 = font_small.render(str(SCORE1), True, RED)
    DISPLAYSURF.blit(scores1, (SCREEN_WIDTH - 30, 10))
    score_coins = font_small.render("Coins: ", True, RED)
    DISPLAYSURF.blit(score_coins, (SCREEN_WIDTH - 100, 10))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
        

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer_music.stop()
        pygame.mixer.Sound('TSIS_8/resources/crash.wav').play()
        time.sleep(1)
        
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (25,150))
        DISPLAYSURF.blit(lose, (150, 300))
          
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        
    if pygame.sprite.spritecollideany(P1, bonus):
        SCORE1 += 1
        SPEED += 0.25
        C1.rect.top = 600
        
    pygame.display.update()
    pygame.display.flip()
    FramePerSec.tick(FPS)
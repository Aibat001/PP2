import pygame
import os

pygame.init()
SIZE = [500, 500]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Player")

playlist = [
    os.path.abspath("TSIS_7/player/musics/Dennis_Loyd_Nevermind.mp3"),
    os.path.abspath("TSIS_7/player/musics/Lil Uzi Vert - XO TOUR Llif3 (DJ Mustard Remix).mp3")
]

running = True


class Player:
    def __init__(self, currSong = 0, isPlaying=True):
        self.currSong = currSong
        self.isPlaying = isPlaying

    def startNewSong(self, path: str):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def unPause(self):
        pygame.mixer.music.unpause()
        self.isPlaying = True

    def pause(self):
        pygame.mixer.music.pause()
        self.isPlaying = False

    def forward(self):
        if self.currSong < len(playlist) - 1:
            self.currSong += 1
        self.startNewSong(playlist[self.currSong])

    def backward(self):
        if self.currSong == 0:
            self.currSong = 0
        else:
            self.currSong -= 1
        self.startNewSong(playlist[self.currSong])

    def drawPlayButton(self):
        playButton = pygame.image.load(os.path.abspath("TSIS_7/player/musics/playButton.png"))
        playButton = pygame.transform.scale(playButton, (100, 100))
        return playButton

    def drawForwardAndBackwardBtns(self):
        forward = pygame.image.load(os.path.abspath("TSIS_7/player/musics/forwardBtn.png"))
        backward = pygame.image.load(os.path.abspath("TSIS_7/player/musics/backward.png"))
        forward = pygame.transform.scale(forward, (100, 100))
        backward = pygame.transform.scale(backward, (100, 100))
        return backward, forward


player = Player(0, True)
player.startNewSong(playlist[0])

backwardBtn, forwardBtn = player.drawForwardAndBackwardBtns()
playBtn = player.drawPlayButton()
font = pygame.font.SysFont("Arial", 16)

while running:
    pygame.time.Clock().tick(10)

    screen.fill((255, 255, 255))
    playBtnC = screen.blit(playBtn, ((screen.get_width() / 2 - 50), 300))
    backwardBtnC = screen.blit(backwardBtn, ((screen.get_width() / 2 - 50 - 100 - 50), 300))
    forwardBtnC = screen.blit(forwardBtn, ((screen.get_width() / 2 - 50 + 100 + 50), 300))

    songTitle = font.render(playlist[player.currSong], True, (0, 0, 0))
    screen.blit(songTitle, ((screen.get_width() / 2 - songTitle.get_width() // 2), 100))

    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player.isPlaying:
                    player.pause()
                else:
                    player.unPause()
            if event.key == pygame.K_RIGHT:
                player.forward()
            if event.key == pygame.K_LEFT:
                player.backward()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if playBtnC.collidepoint(pos):
                if player.isPlaying:
                    player.pause()
                else:
                    player.unPause()
            if forwardBtnC.collidepoint(pos):
                player.forward()
            if backwardBtnC.collidepoint(pos):
                player.backward()

pygame.quit()
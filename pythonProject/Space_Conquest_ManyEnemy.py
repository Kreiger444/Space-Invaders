import pygame
import random
import math
from pygame import mixer
pygame.init()
clock= pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))

mixer.music.load('intense background music.mp3')
mixer.music.play(-1)

pygame.display.set_caption("Space Conquest")
icon = pygame.image.load('spaceship (2).png')
pygame.display.set_icon(icon)

bg = pygame.image.load('background space.jpg')

playerImg = pygame.image.load('spaceship (3).png')
playerX = 368
playerY = 520
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(10)
    enemyX_change.append(0.2)
    enemyY_change.append(0.05)

bulletImg = pygame.image.load('missile.png')
bulletX = 0
bulletY = 520
bulletY_change = 0.6
bullet_state = "ready"

score_value=0
font = pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

over_font = pygame.font.Font('freesansbold.ttf',128)

def show_score(x,y):
    score= font.render("Score: " +str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text= font.render("GAME OVER",True, (255,255,255))
    screen.blit(over_text,(300,270))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


k = 0.15
score = 0
running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound= mixer.Sound('Star Wars Blaster sound effect-[AudioTrimmer.com].mp3')
                    pygame.mixer.music.set_volume(0.05)
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        if enemyY[i]>520:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break


        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 0.15
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -0.15
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('MR.BEAST EXPLOSION SOUND EFFECT-[AudioTrimmer.com].mp3')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i]=random.randint(0,800)
            enemyY[i]=10

        enemy(enemyX[i], enemyY[i], i)
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]


    playerX += playerX_change

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()

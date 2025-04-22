import pygame
import random
import math
import os
from pygame import mixer
from pygame.time import Clock

pygame.init()

Width = 800
Height = 500
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Space Invadors")
background = pygame.image.load('background.project.jpg')
background = pygame.transform.scale(background, (800,500))
clock = pygame.time.Clock()

sound = pygame.mixer.Sound('spaceinvaders1.mpeg')
sound.play()
playerImg = pygame.image.load("player.project.jpg")
playerX = 370
playerY = 380
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy1.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bullet.project.png')
bulletX = 0
bulletY = 380
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score_value = 0

if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
high_score = 0

with open("highscore.txt", "w") as file:
    file.write(str(high_score))

font = pygame.font.Font(None, 32)
textX = 10
textY = 10



game_won = False
game_over = False

win_font = pygame.font.Font(None, 64)
def you_win():
    win_text = win_font.render("YOU WIN!", True, (255,255,0))
    screen.blit(win_text, (250,250))


over_font = pygame.font.Font(None, 64)

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    high = font.render("High score: " + str(high_score), True, (255, 255, 0))
    screen.blit(score, (x,y))
    screen.blit(high, (x,y + 30))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def game_instructions():
    over_text = over_font.render("Controls: SPACEBAR TO SHOOT", True, (255, 255, 255))
    screen.blit(over_text, (5, 10))
    over_text = over_font.render("LEFT AND RIGHT ARROWS TO MOVE", True, (255, 255, 255))
    screen.blit(over_text, (5, 100))


def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

start_time = pygame.time.get_ticks()
running = True
Intro = True
while running:

    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    current_time = pygame.time.get_ticks()
    if (current_time - start_time) < 6000:
        game_instructions()
    else:
        screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_won and not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bulletSound = mixer.Sound("shoot.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

    if not game_won and not game_over:
        playerX += playerX_change
        playerX = max(0, min(playerX, 736))

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            if bulletY <= 0:
                bulletY = 380
                bullet_state = "ready"

        for i in range(num_of_enemies):
            if enemyY[i] > 340:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                game_over = True
                break
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            enemy(enemyX[i], enemyY[i], i)


            if collision(enemyX[i], enemyY[i], bulletX, bulletY):
                explosionSound = mixer.Sound("invaderkilled.wav")
                explosionSound.play()
                bulletY = 380
                bullet_state = "ready"
                score_value += 1

                if score_value > high_score:
                    high_score = score_value
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))

                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            if score_value >= 13:
                game_won = True


        player(playerX, playerY)
        show_score(textX, textY)

        if game_won:
            you_win()
        if bulletY <= 0:
            bulletY = 380
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            if bulletY <= 0:
                bulletY = 380
                bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    if game_won:
        you_win()
        running = False

    elif game_over:
        game_over_text()
        running = False


    pygame.display.update()
    clock.tick(60)
pygame.time.wait(2000)
pygame.quit()






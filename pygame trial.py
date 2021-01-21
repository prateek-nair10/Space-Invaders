import pygame
import random
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()
# create the screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)
highscores = open("leaderboard.py", "a+")

# player
playerImg = pygame.image.load('space-invaders.png')
playerX = 371
playerY = 480
playerXchange = 0
playerYchange = 0

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY
bulletXchange = 0
bulletYchange = 0
bullet_state = "ready"

# music
pygame.mixer.music.load("Voodoo_Like_You_Do.mp3")
pygame.mixer.music.play()

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
num_of_enemies = 5
# deadghost.append(pygame.image.load('deadghost.png'))
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('deadghost.png'))
    enemyX.append(random.randint(0, 730))
    enemyY.append(25)
    enemyXchange.append(0.3)
    enemyYchange.append(0)


def player():
    screen.blit(playerImg, (playerX, playerY))


def enemy(enemyImg, x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bulletImg, (x, y))


# collision
def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if distance < 29:
        return True
    else:
        return False


score_value = 0
x = 0
lvl = 0
lvldup = False
# font
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over font
over_font = pygame.font.Font('freesansbold.ttf', 64)
over_fontX = 200
over_fontY = 200

# lvl font
lvl_font = pygame.font.Font('freesansbold.ttf', 32)
lvl_fontX = 710
lvl_fontY = 10

# highscore font
hs_font = pygame.font.Font('freesansbold.ttf', 54)
hs_fontX = 200
hs_fontY = 300


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_lvl():
    lvl_show = lvl_font.render("lvl:" + str(lvl), True, (255, 255, 255))
    screen.blit(lvl_show, (lvl_fontX, lvl_fontY))


def game_over_font(x, y):
    over = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over, (x, y))
    # highscore
    import leaderboard
    try:
        if leaderboard.h < score_value:  # here "h.highscore" is no. of attempts
            print("New Highscore!!!")
            hs = hs_font.render("New Highscore!!", True, (255, 255, 255))
            screen.blit(hs, (hs_fontX, hs_fontY))
            s = str(score_value)
            ins = "h=" + s + "\n"
            highscores.write(ins)
            highscores.close()

        else:
            print(".")

    except:  # handles variable "h" not defined error
        print("New Highscore!!!")
        hs = hs_font.render("New Highscore!!", True, (255, 255, 255))
        screen.blit(hs, (hs_fontX, hs_fontY))
        s = str(score_value)
        ins = "h=" + s + "\n"
        highscores.write(ins)
        highscores.close()


###################
#########Game loop
running = True

while running:
    # RGB
    screen.fill((20, 0, 190))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerXchange = 0.6
            if event.key == pygame.K_LEFT:
                playerXchange = -0.6
            if event.key == pygame.K_UP:
                playerY -= 17
            if event.key == pygame.K_DOWN:
                playerY += 17
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = pygame.mixer.Sound("Gun_Silencer.wav")
                    bullet_sound.play()
                    bulletX = playerX + 7
                    bulletY = playerY + 7
                    bullet_state = "fired"


    #bullet
    if bullet_state == "fired":
        fire_bullet(bulletX, bulletY)
        bulletYchange = -0.9 - (lvl * 0.02)
        bulletY += bulletYchange

        if bulletY < 0:
            bullet_state = "ready"
            bulletYchange = 0

    if playerX < 20.0:
        playerX = 20
    elif playerX > 720:
        playerX = 720
    else:
        playerX += playerXchange

    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_font(over_fontX, over_fontY)
            break

        # enemy
        if enemyX[i] < 0:
            alt = enemyXchange[i]
            enemyX[i] = 0
            enemyXchange[i] = -alt
            enemyY[i] += 20
        elif enemyX[i] > 734:
            alt = enemyXchange[i]
            enemyXchange[i] = -alt
            enemyY[i] += 20

        enemyX[i] += enemyXchange[i]
        # collision check
        if isCollision(bulletX, bulletY, enemyX[i], enemyY[i]):
            enemyX[i] = random.randint(1, 730)
            enemyY[i] = 30
            score_value += 1

        # game over
        if isCollision(playerX, playerY, enemyX[i], enemyY[i]):
            game_over_font(over_fontX, over_fontY)
            running = False

        enemy(enemyImg[i], enemyX[i], enemyY[i])


    # lvl up
    if score_value % 10 == 0:
        if score_value != x:
            lvldup = False
        if lvldup != True:
            lvl += 1
            num_of_enemies += 1
            enemyImg.append(pygame.image.load('aliveghost.png'))
            enemyX.append(random.randint(0, 730))
            enemyY.append(25)
            enemyXchange.append(-0.3)
            enemyYchange.append(0)
            for i in range(num_of_enemies):
                if enemyXchange[i] > 0:
                    enemyXchange[i] += 0.03
                else:
                    enemyXchange[i] -= 0.03
                bulletYchange -= 0.02
            lvldup = True
            x = score_value

    player()

    show_score(textX, textY)
    show_lvl()

    pygame.display.update()

import pygame
import random
import time
import math

# 1. ИСПРАВЛЕНО: Добавлены скобки для вызова функции init
pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

clock = pygame.time.Clock()

block_size = 20
FPS = 10

font = pygame.font.SysFont(None, 25)

def snake(block_size, snakeList):
    for XnY in snakeList:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def message_to_screen(msg, color, y_displace=0):
    screen_text = font.render(msg, True, color)
    # Смещение по Y, чтобы текст не накладывался друг на друга
    gameDisplay.blit(screen_text, [display_width / 4, display_height / 2 + y_displace])

def game_loop():
    gameExit = False
    gameOver = False

    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    # Яблоко генерируется кратно block_size (20), чтобы координаты идеально совпадали
    randAppleX = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
    randAppleY = round(random.randrange(0, display_height - block_size) / 20.0) * 20.0

    while not gameExit: 
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game Over", red, -30)
            message_to_screen("Press C to play again or Q to quit", black, 10)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        # 3. ИСПРАВЛЕНО: Безопасный перезапуск без рекурсии
                        game_loop() 
                        return 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)

        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)
        pygame.display.update()

        # 1. ИСПРАВЛЕНО: Простое и точное сравнение координат головы и яблока
        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
            randAppleY = round(random.randrange(0, display_height - block_size) / 20.0) * 20.0
            snakeLength += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

game_loop()

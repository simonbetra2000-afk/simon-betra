import pygame
import random

# Инициализация Pygame и шрифтов
pygame.init()
pygame.font.init()

# Настройки окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SUPER ARKANOID")
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.SysFont("Arial", 64, bold=True)
font_medium = pygame.font.SysFont("Arial", 40, bold=True)
font_small = pygame.font.SysFont("Arial", 24)

# Состояния игры: 'MENU', 'GAME', 'GAME_OVER', 'WIN'
game_state = 'MENU'
score = 0

# Настройки платформы
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 15
platform_x = (WIDTH - PLATFORM_WIDTH) // 2
platform_y = HEIGHT - 40
platform_speed = 10

# Настройки мяча
BALL_RADIUS = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 0
ball_speed_y = 0

# Настройки блоков
BLOCK_ROWS = 5
BLOCK_COLS = 10
BLOCK_WIDTH = 72
BLOCK_HEIGHT = 20
BLOCK_PADDING = 6
OFFSET_X = 15
OFFSET_Y = 60

# Цвета для рядов блоков
ROW_COLORS = [
    (255, 50, 50),   # Красный
    (255, 120, 0),   # Оранжевый
    (255, 200, 0),   # Желтый
    (50, 200, 50),   # Зеленый
    (50, 150, 255)   # Голубой
]

blocks = []

def init_game():
    """Сброс всех переменных для начала новой игры"""
    global platform_x, ball_x, ball_y, ball_speed_x, ball_speed_y, blocks, score, game_state
    
    score = 0
    platform_x = (WIDTH - PLATFORM_WIDTH) // 2
    
    ball_x = WIDTH // 2
    ball_y = HEIGHT - 100
    
    # Случайное направление вверх
    ball_speed_y = -5
    ball_speed_x = random.choice([-4, -3, 3, 4])
    
    # Генерация блоков с цветами
    blocks = []
    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            b_x = OFFSET_X + col * (BLOCK_WIDTH + BLOCK_PADDING)
            b_y = OFFSET_Y + row * (BLOCK_HEIGHT + BLOCK_PADDING)
            color = ROW_COLORS[row % len(ROW_COLORS)]
            # Сохраняем Rect и его цвет
            blocks.append({'rect': pygame.Rect(b_x, b_y, BLOCK_WIDTH, BLOCK_HEIGHT), 'color': color})
            
    game_state = 'GAME'

# Главный цикл игры
running = True
while running:
    # --- ОБРАБОТКА НАЖАТИЙ (EVENTS) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if game_state == 'MENU':
                if event.key == pygame.K_SPACE:
                    init_game()
            elif game_state in ['GAME_OVER', 'WIN']:
                if event.key == pygame.K_r:  # R - рестарт
                    init_game()
                if event.key == pygame.K_ESCAPE:  # ESC - выход в меню
                    game_state = 'MENU'

    # --- ЛОГИКА ИГРЫ (UPDATE) ---
    if game_state == 'GAME':
        # Движение платформы
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and platform_x > 0:
            platform_x -= platform_speed
        if keys[pygame.K_RIGHT] and platform_x < WIDTH - PLATFORM_WIDTH:
            platform_x += platform_speed

        # Движение мяча
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Хитбокс мяча для столкновений
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

        # Отскок от стен
        if ball_x <= BALL_RADIUS or ball_x >= WIDTH - BALL_RADIUS:
            ball_speed_x = -ball_speed_x
        if ball_y <= BALL_RADIUS:
            ball_speed_y = -ball_speed_y

        # Отскок от платформы (с физикой угла)
        platform_rect = pygame.Rect(platform_x, platform_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        if ball_speed_y > 0 and ball_rect.colliderect(platform_rect):
            # Вычисляем, куда именно ударил мяч относительно центра платформы
            relative_intersect_x = (platform_x + (PLATFORM_WIDTH / 2)) - ball_x
            normalized_intersect_x = relative_intersect_x / (PLATFORM_WIDTH / 2)
            
            # Меняем угол отскока по X в зависимости от места удара
            ball_speed_x = -normalized_intersect_x * 6
            ball_speed_y = -ball_speed_y

        # Расчет столкновений с блоками
        for block in blocks[:]:
            if ball_rect.colliderect(block['rect']):
                b = block['rect']
                # Физика отскока от блока
                if abs(ball_rect.bottom - b.top) < 7 and ball_speed_y > 0:
                    ball_speed_y = -ball_speed_y
                elif abs(ball_rect.top - b.bottom) < 7 and ball_speed_y < 0:
                    ball_speed_y = -ball_speed_y
                elif abs(ball_rect.right - b.left) < 7 and ball_speed_x > 0:
                    ball_speed_x = -ball_speed_x
                elif abs(ball_rect.left - b.right) < 7 and ball_speed_x < 0:
                    ball_speed_x = -ball_speed_x

                blocks.remove(block)
                score += 10
                break

        # Проверка поражения
        if ball_y >= HEIGHT:
            game_state = 'GAME_OVER'

        # Проверка победы
        if not blocks:
            game_state = 'WIN'

    # --- ОТРИСОВКА ЭКРАНОВ (DRAW) ---
    screen.fill((25, 25, 40))  # Красивый темно-синий фон

    if game_state == 'MENU':
        # Экран главного меню
        txt_title = font_large.render("SUPER ARKANOID", True, (0, 255, 200))
        txt_start = font_medium.render("Нажми ПРОБЕЛ для старта", True, (255, 255, 255))
        
        screen.blit(txt_title, (WIDTH // 2 - txt_title.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(txt_start, (WIDTH // 2 - txt_start.get_width() // 2, HEIGHT // 2 + 30))

    elif game_state == 'GAME':
        # Отрисовка игрового процесса
        # Рисуем блоки
        for block in blocks:
            pygame.draw.rect(screen, block['color'], block['rect'], border_radius=4)
            # Небольшая обводка для стиля
            pygame.draw.rect(screen, (30, 30, 30), block['rect'], 1, border_radius=4)

        # Платформа и мяч
        pygame.draw.rect(screen, (0, 200, 250), (platform_x, platform_y, PLATFORM_WIDTH, PLATFORM_HEIGHT), border_radius=5)
        pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), BALL_RADIUS)

        # Отображение счета
        txt_score = font_small.render(f"SCORE: {score}", True, (255, 255, 255))
        screen.blit(txt_score, (20, 15))

    elif game_state == 'GAME_OVER':
        # Экран поражения
        txt_lose = font_large.render("ВЫ ПРОИГРАЛИ!", True, (255, 50, 50))
        txt_score = font_medium.render(f"Ваш счет: {score}", True, (255, 255, 255))
        txt_hint = font_small.render("Нажми [R] для рестарта | [ESC] для меню", True, (150, 150, 150))
        
        screen.blit(txt_lose, (WIDTH // 2 - txt_lose.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(txt_score, (WIDTH // 2 - txt_score.get_width() // 2, HEIGHT // 2))
        screen.blit(txt_hint, (WIDTH // 2 - txt_hint.get_width() // 2, HEIGHT // 2 + 100))

    elif game_state == 'WIN':
        # Экран победы
        txt_win = font_large.render("ЧЁТКАЯ ПОБЕДА!", True, (50, 255, 50))
        txt_score = font_medium.render(f"Итоговый счет: {score}", True, (255, 255, 255))
        txt_hint = font_small.render("Нажми [R] чтобы сыграть еще раз | [ESC] для меню", True, (150, 150, 150))
        
        screen.blit(txt_win, (WIDTH // 2 - txt_win.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(txt_score, (WIDTH // 2 - txt_score.get_width() // 2, HEIGHT // 2))
        screen.blit(txt_hint, (WIDTH // 2 - txt_hint.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

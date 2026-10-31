import pygame
import random
import sys

# Инициализация
pygame.init()

# Настройки экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический Защитник")
clock = pygame.time.Clock()

# Цвета
BLACK = (10, 10, 15)
WHITE = (255, 255, 255)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
BLUE = (52, 152, 219)

def draw_text(text, size, x, y):
    font = pygame.font.SysFont("Arial", size, bold=True)
    render = font.render(text, True, WHITE)
    rect = render.get_rect(center=(x, y))
    screen.blit(render, rect)

def main():
    # Игрок (Корабль)
    player_w, player_h = 50, 40
    player_x = WIDTH // 2 - player_w // 2
    player_y = HEIGHT - 60
    player_speed = 7
    lives = 3
    score = 0

    # Лазеры (Пули)
    bullets = []
    bullet_speed = -10

    # Враги (Пришельцы)
    enemy_w, enemy_h = 40, 30
    enemies = []
    enemy_speed = 3

    # Функция создания нового врага
    def spawn_enemy():
        x = random.randint(0, WIDTH - enemy_w)
        y = random.randint(-150, -40)
        enemies.append(pygame.Rect(x, y, enemy_w, enemy_h))

    # Создаем первых врагов
    for _ in range(8):
        spawn_enemy()

    game_over = False

    # Игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    main() # Перезапуск
                elif not game_over and event.key == pygame.K_SPACE:
                    # Стрельба: создаем пулю из носа корабля
                    bullet = pygame.Rect(player_x + player_w // 2 - 2, player_y, 4, 15)
                    bullets.append(bullet)

        if not game_over:
            # Управление кораблем (Стрелочки)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_w:
                player_x += player_speed

            # Движение пуль
            for b in bullets[:]:
                b.y += bullet_speed
                if b.y < 0:
                    bullets.remove(b)

            # Движение врагов
            for e in enemies[:]:
                e.y += enemy_speed
                
                # Если враг долетел до низа экрана
                if e.y > HEIGHT:
                    enemies.remove(e)
                    spawn_enemy()
                    lives -= 1
                    if lives <= 0:
                        game_over = True

                # Проверка столкновения врага с кораблем игрока
                player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
                if player_rect.colliderect(e):
                    enemies.remove(e)
                    spawn_enemy()
                    lives -= 1
                    if lives <= 0:
                        game_over = True

            # Проверка попадания пули во врага
            for b in bullets[:]:
                for e in enemies[:]:
                    if b.colliderect(e):
                        if b in bullets:
                            bullets.remove(b)
                        enemies.remove(e)
                        spawn_enemy()
                        score += 10
                        # Немного увеличиваем сложность со временем
                        if score % 100 == 0:
                            enemy_speed += 0.5

        # --- ОТРИСОВКА ---
        screen.fill(BLACK)

        if not game_over:
            # Рисуем игрока (треугольный корабль)
            pygame.draw.polygon(screen, GREEN, [
                (player_x + player_w // 2, player_y), 
                (player_x, player_y + player_h), 
                (player_x + player_w, player_y + player_h)
            ])

            # Рисуем пули
            for b in bullets:
                pygame.draw.rect(screen, YELLOW, b)

            # Рисуем врагов
            for e in enemies:
                pygame.draw.rect(screen, RED, e, border_radius=5)

            # Интерфейс
            draw_text(f"Счёт: {score}", 20, 60, 20)
            draw_text(f"Жизни: {lives}", 20, WIDTH - 60, 20)
        else:
            # Экран конца игры
            draw_text("КОРАБЛЬ УНИЧТОЖЕН", 40, WIDTH // 2, HEIGHT // 2 - 40)
            draw_text(f"Ваш результат: {score} очков", 24, WIDTH // 2, HEIGHT // 2 + 10)
            draw_text("Нажмите ПРОБЕЛ для новой битвы", 18, WIDTH // 2, HEIGHT // 2 + 60)

        pygame.display.flip()
        clock.tick(60) # 60 FPS для максимальной плавности

if __name__ == "__main__":
    main()


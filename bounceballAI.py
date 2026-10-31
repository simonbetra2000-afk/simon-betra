import pygame
import math
import random

pygame.init()

# Формат TikTok (вертикальный экран)
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TikTok Layer Escape")
clock = pygame.time.Clock()

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Безопасная функция для генерации цвета
def get_rainbow_color(step, total_steps):
    frequency = 2 * math.pi / total_steps
    # Считаем и принудительно обрезаем до диапазона 0-255
    r = max(0, min(255, int(127 + 128 * math.sin(frequency * step))))
    g = max(0, min(255, int(127 + 128 * math.sin(frequency * step + 2 * math.pi / 3))))
    b = max(0, min(255, int(127 + 128 * math.sin(frequency * step + 4 * math.pi / 3))))
    return (r, g, b)

class Layer:
    def __init__(self, radius, speed, color, thickness=12):
        self.radius = radius
        self.speed = speed  # Положительная — вправо, отрицательная — влево
        self.color = color
        self.thickness = thickness
        self.current_angle = random.uniform(0, 2 * math.pi)
        self.gate_size = math.radians(45)  # Размер дырки (ворот)
        self.active = True

    def update(self):
        if not self.active:
            return
        self.current_angle += self.speed
        self.current_angle %= (2 * math.pi)

    def draw(self, surface):
        if not self.active:
            return

        points = []
        # Дырка находится между current_angle и (current_angle + gate_size)
        # Рисуем саму стену (всё остальное пространство окружности)
        start_draw_angle = self.current_angle + self.gate_size
        end_draw_angle = self.current_angle + 2 * math.pi
        
        step = 0.04
        a = start_draw_angle
        while a <= end_draw_angle:
            x = CENTER_X + math.cos(a) * self.radius
            y = CENTER_Y + math.sin(a) * self.radius
            points.append((x, y))
            a += step
            
        if len(points) >= 2:
            pygame.draw.lines(surface, self.color, False, points, self.thickness)

class Ball:
    def __init__(self):
        self.x = CENTER_X
        self.y = CENTER_Y
        self.radius = 8
        self.speed = 5
        
        # Начальный случайный вектор движения
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        self.flash_timer = 0
        
        # Индекс слоя, внутри которого СЕЙЧАС заперт мяч (начинаем с самого маленького — 0)
        self.current_layer_idx = 0

    def update(self, layers):
        self.x += self.vx
        self.y += self.vy

        if self.flash_timer > 0:
            self.flash_timer -= 1

        # Если все слои пройдены, просто отскакиваем от краев экрана
        if self.current_layer_idx >= len(layers):
            if self.x <= self.radius or self.x >= WIDTH - self.radius:
                self.vx = -self.vx
            if self.y <= self.radius or self.y >= HEIGHT - self.radius:
                self.vy = -self.vy
            return

        # Проверяем взаимодействие ТОЛЬКО с тем слоем, внутри которого заперт мяч
        layer = layers[self.current_layer_idx]
        
        dx = self.x - CENTER_X
        dy = self.y - CENTER_Y
        distance = math.hypot(dx, dy)

        # Мяч касается внутренней границы текущего слоя
        if distance + self.radius >= layer.radius - layer.thickness / 2:
            # Находим угол мяча относительно центра
            ball_angle = math.atan2(dy, dx)
            if ball_angle < 0:
                ball_angle += 2 * math.pi

            # Находим относительный угол мяча в системе координат крутящегося слоя
            relative_angle = (ball_angle - layer.current_angle) % (2 * math.pi)

            # Вектор нормали для отскока
            nx = dx / distance
            ny = dy / distance

            # ПРОВЕРКА: Попал ли мяч ровно в дырку (ворота)?
            if relative_angle <= layer.gate_size:
                # ЧЁТКО! Попал в дырку! Слой уничтожается (отслаивается)
                layer.active = False
                self.flash_timer = 5  # Эффект вспышки
                
                # Мяч переходит на следующий (более широкий) слой
                self.current_layer_idx += 1
                
                # При переходе даем мячу пинок скорости для экшена
                self.vx *= 1.05
                self.vy *= 1.05
            else:
                # Не попал в дырку — обычный физичный отскок внутрь кольца
                dot_product = self.vx * nx + self.vy * ny
                self.vx = self.vx - 2 * dot_product * nx
                self.vy = self.vy - 2 * dot_product * ny
                
                # Выталкиваем мяч обратно внутрь кольца, чтобы не залипал
                self.x = CENTER_X + nx * (layer.radius - layer.thickness / 2 - self.radius - 1)
                self.y = CENTER_Y + ny * (layer.radius - layer.thickness / 2 - self.radius - 1)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

# --- СОЗДАНИЕ СЛОЕВ (ОТ МЕНЬШЕГО К БОЛЬШЕМУ) ---
layers = []
num_layers = 12
start_radius = 40
radius_step = 24

for i in range(num_layers):
    radius = start_radius + i * radius_step
    # Чередуем вращение слоев для залипательности
    speed = 0.02 if i % 2 == 0 else -0.02
    color = get_rainbow_color(i, num_layers)
    layers.append(Layer(radius, speed, color))

ball = Ball()

# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Рестарт на ПРОБЕЛ
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            for l in layers:
                l.active = True
            ball = Ball()

    # Обновление
    for layer in layers:
        layer.update()
    ball.update(layers)

    # Отрисовка
    if ball.flash_timer > 0:
        screen.fill((40, 40, 55))  # Вспышка при пробитии слоя
    else:
        screen.fill((10, 10, 15))

    # Рисуем слои
    for layer in layers:
        layer.draw(screen)

    # Рисуем мяч
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

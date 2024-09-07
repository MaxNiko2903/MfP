import pygame
import sys
import requests
from io import BytesIO
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Определяем размеры окна и создаем его
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Простой Арканоид')

# Определяем цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Загрузка изображения
response = requests.get("https://cdn.icon-icons.com/icons2/37/PNG/512/DVD_4193.png")
img = pygame.image.load(BytesIO(response.content))
img = pygame.transform.scale(img, (50, 50))  # Устанавливаем размер изображения

# Настраиваем шрифты
font = pygame.font.SysFont(None, 36)
start_button = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 - 20, 100, 40)

# Инициализация переменных для мяча и шлейфа
ball_x, ball_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
ball_dx, ball_dy = 5, -5
ball_active = False
trail = []

# Основной игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                ball_active = True
                start_button = pygame.Rect(-100, -100, 0, 0)  # Убираем кнопку

    # Логика движения мяча
    if ball_active:
        ball_x += ball_dx
        ball_y += ball_dy

        # Добавляем шлейф
        trail.append((ball_x, ball_y))
        if len(trail) > 10:
            trail.pop(0)

        # Отражение мяча от границ окна
        if ball_x - img.get_width() / 2 < 0 or ball_x + img.get_width() / 2 > WINDOW_WIDTH:
            ball_dx = -ball_dx
        if ball_y - img.get_height() / 2 < 0 or ball_y + img.get_height() / 2 > WINDOW_HEIGHT:
            ball_dy = -ball_dy

    # Рисуем объекты
    window.fill(BLACK)

    # Рисуем шлейф
    for (tx, ty) in trail:
        pygame.draw.circle(window, RED, (int(tx), int(ty)), 5)

    # Рисуем изображение мяча
    window.blit(img, (int(ball_x) - img.get_width() // 2, int(ball_y) - img.get_height() // 2))

    # Рисуем кнопку "Пуск" только если она активна
    if start_button.x != -100:
        pygame.draw.rect(window, RED, start_button)
        text_surface = font.render('Пуск', True, BLACK)
        window.blit(text_surface, (start_button.x + 20, start_button.y + 5))

    # Обновляем экран
    pygame.display.flip()
    pygame.time.Clock().tick(60)

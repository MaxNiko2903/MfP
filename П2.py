import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид с мячиками")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Класс мячика
class Ball:
    def __init__(self, x, y, radius, color, angle):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 5
        self.angle = angle

    def move(self):
        # Перемещение мячика
        self.x += self.speed * math.cos(self.angle)
        self.y -= self.speed * math.sin(self.angle)

        # Проверка на отскок от стен
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.angle = math.pi - self.angle  # Отскок по горизонтали

        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.angle = -self.angle  # Отскок по вертикали

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Функция для проверки столкновений между мячиками
def check_collision(ball1, ball2):
    distance = math.sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)
    if distance <= ball1.radius + ball2.radius:
        # Меняем направление мячиков при столкновении
        ball1.angle, ball2.angle = ball2.angle, ball1.angle

# Главное меню
def main_menu():
    font = pygame.font.SysFont(None, 36)
    # Разделили текст на две строки
    text1 = font.render("Нажмите '1' для режима без столкновений", True, WHITE)
    text2 = font.render("Нажмите '2' для режима со столкновениями", True, WHITE)

    screen.fill(BLACK)
    screen.blit(text1, (WIDTH // 6, HEIGHT // 2 - 50))
    screen.blit(text2, (WIDTH // 6, HEIGHT // 2 + 10))  # Вторая строка ниже первой
    pygame.display.flip()

    mode = 0
    while mode not in [1, 2]:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = 1
                elif event.key == pygame.K_2:
                    mode = 2
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
    return mode

# Основная игра
def game(mode):
    # Создаем два мячика. В режиме без столкновений они на разных уровнях.
    if mode == 1:
        ball1 = Ball(100, 150, 20, WHITE, math.radians(45))  # Нижний уровень
        ball2 = Ball(700, 450, 20, WHITE, math.radians(135))  # Верхний уровень
    else:
        ball1 = Ball(100, 100, 20, WHITE, math.radians(45))  # Одинаковый уровень
        ball2 = Ball(700, 100, 20, WHITE, math.radians(135))

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Движение мячиков
        ball1.move()
        ball2.move()

        # Рисуем мячики
        ball1.draw(screen)
        ball2.draw(screen)

        # Проверяем столкновения только в режиме со столкновениями
        if mode == 2:
            check_collision(ball1, ball2)

        # Обновляем экран
        pygame.display.flip()

        # Задержка для 60 FPS
        clock.tick(60)

# Запуск программы
while True:
    mode = main_menu()
    game(mode)
